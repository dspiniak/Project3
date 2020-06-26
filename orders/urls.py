from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register_view, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("load_sizes", views.load_sizes, name="load_sizes"),
    path("load_toppings", views.load_toppings, name="load_toppings"),
    path("shopping_cart", views.shopping_cart,name="shopping_cart"),
    path("your_orders", views.your_orders,name="your_orders"),
    path("users_orders", views.users_orders,name="users_orders"),
    path("change_cart_status", views.change_cart_status, name="change_cart_status"),

]
