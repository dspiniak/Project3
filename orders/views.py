from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .models import FoodType, Size, Topping, BasePrice, ToppingPrice, Order, ShoppingCart
from django.core import serializers
from django.views.decorators.http import require_http_methods

# USER VIEWS
def index(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            # get dishes from menu model and render them
            context = {
                "food_type": FoodType.objects.all()
                }
            return render(request, "index.html", context)

        if request.method == "POST":

            username = request.user
            food_type_id = request.POST["food_type"].split(':')[0]
            if request.POST["size"]:
                size = request.POST["size"]
            if request.POST.getlist("toppings"):
                toppings = request.POST.getlist("toppings")

            food_category = FoodType.objects.get(id=food_type_id).category
            # order_price = request.POST["order_price"]
            print(f"{username}, {food_type_id}, {size}, {toppings}")

            # get order price via size and toppings when appropiate


            # get base price
            if "Pizza" or "Sub" or "Dinner Platters" in food_category:
                size_id = Size.objects.get(size=size.split(',')[0]).id
                base_price = BasePrice.objects.get(food_id=food_type_id,size=size_id).price
            else:
                base_price = BasePrice.objects.get(food_id=food_type_id).price

            # get toppings price
            if "Pizza" in food_category:
                topping_price = ToppingPrice.objects.get(food=food_type_id,size_id=size_id,topping_num=len(toppings)).price
            elif "Sub" in food_category:
                topping_price = ToppingPrice.objects.get(food=food_type_id,topping_num=len(toppings)).price
            else:
                topping_price = 0

            order_price=base_price+topping_price
            print(f"order price is: ${order_price}")

            # create order in model
            order = Order(username=username, food_type_id=food_type_id, size_id=size_id, order_price=order_price)
            order.save()

            toppings = Topping.objects.filter(topping__in=toppings)
            # print(toppings)
            order.toppings.set(toppings)

            # create shopping cart or add order to shopping cart
            if not ShoppingCart.objects.filter(username=username, status="unconfirmed"):

                # create shopping cart if none created
                shopping_cart = ShoppingCart(username=username, total_price=order_price, status="unconfirmed")
                shopping_cart.save()
                shopping_cart.orders.add(order)

            else:
                # add order to shopping cart
                shopping_cart = ShoppingCart.objects.get(username=username, status="unconfirmed")
                shopping_cart.orders.add(order)
                old_total_price = shopping_cart.total_price
                shopping_cart.total_price = old_total_price + order_price
                shopping_cart.save()

            return HttpResponseRedirect(reverse("index"))

    else:
        return HttpResponseRedirect(reverse("login"), {"message": "please login before making an order"})


def shopping_cart(request):

    if request.user.is_authenticated:

        # get orders
        username = request.user
        orders = Order.objects.filter(username=username, shoppingcart__status="unconfirmed")

        try:
            shopping_cart = ShoppingCart.objects.get(username=username, status="unconfirmed")
            print(shopping_cart)
        except ShoppingCart.DoesNotExist:
            shopping_cart = None

        if request.method == "GET":

            # pass orders and total_price to context
            if shopping_cart:

                print(shopping_cart)
                context = {
                    "orders": orders,
                    "total_price": shopping_cart.total_price,
                    "shopping_cart": shopping_cart
                    }

                return render(request, "shopping_cart.html", context)

            else:
                print("No shopping cart")
                return render(request, "shopping_cart.html", {"message": "You have no items in the shopping cart yet"})

        if request.method == "POST":

            # check if user succesfully pressed confirm order button
            if request.POST["order_confirmed"]=="confirmed":

                shopping_cart.status = "pending"
                shopping_cart.save()

                return render(request, "shopping_cart.html", {"message": "Your order has been sent to Pinnochio's Pizzas & Subs"})
        else:
            return HttpResponseRedirect(reverse("shopping_cart"), {"message": "there was an error submitting your order, please contact Pinnochio's or try again"})
    else:
        return HttpResponseRedirect(reverse("login"), {"message": "please login before making an order"})


def your_orders(request):
    if request.user.is_authenticated:

        username=request.user
        shopping_carts = ShoppingCart.objects.filter(username=username).exclude(status="unconfirmed")

        if request.method == "GET":

            # pass shopping_cart to context
            context = {
                "shopping_carts": shopping_carts
                }

            return render(request, "your_orders.html", context)


# send menu options to client
@require_http_methods(["POST"])
def load_sizes(request):

    # get selected choice and obtain food id
    choice = request.POST['food_choice']
    print(f"received food choice from client: {choice}")
    food_id = choice.split(':')[0]

    # construct json object with size and price via food id
    sizes_query = BasePrice.objects.filter(food=food_id)
    print(f"converted size and price to query: {sizes_query}")
    sizes_json = serializers.serialize("json", sizes_query, use_natural_foreign_keys=True, use_natural_primary_keys=True, fields=["size","price"])
    print(f"converted size and price to json: {sizes_json}")

    # insert size and prices in json object for HttpResponse
    data = {
        "sizes": sizes_json
    }
    return JsonResponse(data)


# send menu options to client
@require_http_methods(["POST"])
def load_toppings(request):

    # get selected food choice and obtain food id
    food_choice = request.POST['food_choice']
    size_choice = request.POST['size_choice']
    print(f"received food choice: {food_choice}")
    print(f"received size choice: {size_choice}")

    if size_choice:
        size_id = Size.objects.get(size=size_choice).id

    food_choice_id = food_choice.split(':')[0]

    # construct json object with toppings
    toppings_query = FoodType.objects.filter(id=food_choice_id)
    print(f"about to send toppings query: {toppings_query}")

    toppings_json = serializers.serialize("json", toppings_query, use_natural_foreign_keys=True, use_natural_primary_keys=True, fields=["toppings","price"])
    print(f"about to send toppings json: {toppings_json}")

    # construct json object with toppings' prices
    if size_choice:
        if "Pizza" in food_choice:
            toppings_prices_query = ToppingPrice.objects.filter(food=food_choice_id,size_id=size_id)
        else:
            toppings_prices_query = ToppingPrice.objects.filter(food=food_choice_id)
        print(f"about to send toppings prices query 1: {toppings_prices_query}")
    else:
        toppings_prices_query = ToppingPrice.objects.filter(food=food_choice_id)
        print(f"about to send toppings prices query 2: {toppings_prices_query}")

    toppings_prices_json = serializers.serialize("json", toppings_prices_query, use_natural_foreign_keys=True, use_natural_primary_keys=True, fields=["topping_num","price"])
    print(f"about to send toppings prices json: {toppings_prices_json}")

    # insert topping and prices in json object for HttpResponse
    data = {
        # get toppings and prices
        "toppings": toppings_json,
        "toppings_prices": toppings_prices_json
    }

    return JsonResponse(data)

# ADMIN VIEWS
# Display all the users orders to admin users
def users_orders(request):

    if request.user.is_authenticated and request.user.is_superuser:
        # get shopping carts, excluding those that are unconfirmed
        shopping_carts = ShoppingCart.objects.exclude(status="unconfirmed")
        print(f"GOT USERS ORDERS FROM DB: {shopping_carts}")
        status_choices = ShoppingCart.status_choices

        # pass data to context
        context = {
            "shopping_carts": shopping_carts,
            "status_choices": status_choices
            }

    return render(request, "users_orders.html", context)

# change the status of the shopping cart
@require_http_methods(["POST"])
def change_cart_status(request):
    if request.user.is_superuser:
        # get client values
        cart_id = request.POST["cart_id"]
        status_selected = request.POST["status_selected"]

        # check if there are orders in shopping cart first
        if ShoppingCart.objects.filter(id=cart_id).count()>=1:
            data = {"message": "User already has orders in the shopping cart, delete the other cart first to change the status"}

        # change shopping cart status
        else:
            shopping_cart = ShoppingCart.objects.get(id=cart_id)
            print(f"OLD SHOPPING CART STATUS: {shopping_cart}")
            shopping_cart.status = status_selected
            shopping_cart.save()
            print(f"new shopping cart status: {ShoppingCart.objects.get(id=cart_id)}")
            # pass success message to client
            data = {"message": "Shopping cart with id "+cart_id+", changed status succesfully to "+status_selected}

    return JsonResponse(data)

# USER AUTH FUNCTIONS
# Register view
def register_view(request):

    # check if user if authenticated
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"), {"message": "user is already registered, logout to register another username"})

    # get form info via POST
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        password_check = request.POST["password_check"]


        # server-side check of form inputs: input of all fields and successful password check
        if not first_name or not last_name or not email or not username or not password or not password_check:
            return render(request, "register.html", {"message": "please enter all required fields"})
        elif password!=password_check:
            return render(request, "register.html", {"message": "passwords don't match"})

        # check if username or email exists
        try:
            duplicate_username = User.objects.get(username=username)
            duplicate_email = User.objects.get(email=email)
            return render(request, "register.html", {"message": "username and/or email already exists"})

        except User.DoesNotExist:
            # create user and commit to database
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
            user.save()

            # login user and redirect to index
            login(request, user)
            return HttpResponseRedirect(reverse("index"), {"message": "user registered"})

    else:
        return render(request, "register.html")


# Login view
def login_view(request):

    if request.method == "POST":
        # get form info via POST
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {"message": "invalid credentials"})

    else:
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return render(request, "login.html", {"message": "user logged out"})

# Logout view
