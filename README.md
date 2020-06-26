# Project 3

Web Programming with Python and JavaScript

*STATIC*
**change_cart_status.js**
Creates a request to server to change the shopping cart status.

**menu.js**
Adds skip logic to display the dishes select buttons and calculates prices.

**style.css**
Stylesheet that adds formatting to the footer, messages, and buttons.

*TEMPLATES*

**base.html**
Base template with the menu. Imports bootstrap 3 and stylesheet.

**index.html**
Displays menu and allows users to add items to shopping cart.

**login.html**
Allows user to login by submitting username via a form.

**register.html**
Allows user to register.

**shopping_cart.html**
Allows user to confirm an order.

**users_orders.html**
Allows admin to view all existing orders.

**your_orders.html**
Allows user to view all existing orders.


*views.py*

Imports http, auth, models, and serializers

`USER FUNCTIONS`

1. index: Initially displays dishes to client, then uses POST to submit order.

2. shopping_cart: passes "unconfirmed" orders to client and confirms orders via POST.

3. your_orders: passes all logged user's orders to client.

4. Auxiliar functions:
  - load_sizes: receives a dish and passes available sizes and base prices to client.
  - load_toppings: receives a dish and size and passes available toppings and prices to client.

`ADMIN FUNCTIONS`

1. users_orders: passes all orders to client

2. Auxiliary function - change_cart_status: changes a cart "status" and returns success or failure to client.

`AUTH FUNCTIONS`

1. login: logins user.

2. register: registers user.

3. logout: logouts user.

*models.py*

Contains the following models:
- FoodType: Dish or Food "Type", e.g. pizza, sub, dessert
- Size, Topping: self explanatory
- BasePrice: Price of the dish + size
- ToppingPrice: Price of the topping
- Order: A dish with its properties
- ShoppingCart: A collection of orders
