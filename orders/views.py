from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .models import FoodType, Size, Topping, BasePrice, ToppingPrice

from django.views.decorators.http import require_http_methods

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            # get items from menu model and render them
            context = {
                "food_type": FoodType.objects.all(),
                "base_price": BasePrice.objects.all(),
                "topping_price": ToppingPrice.objects.all()
            }
                # get elements from model
            return render(request, "index.html", context)
    else:
        return HttpResponseRedirect(reverse("login"), {"message": "please login before making an order"})


# send menu options to server
# @require_http_methods(["POST"])
def load_options(request):
    choice = request.POST['choice']
    if "Regular Pizza" in choice:
        data = {
            # get sizes and prices
            "size_price": BasePrice.objects.filter(food=choice)
            # get toppings and prices
        }
        return JsonResponse(data)

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
