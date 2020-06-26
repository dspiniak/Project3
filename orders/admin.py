from django.contrib import admin

from .models import BasePrice, FoodType, Size, Topping, ToppingPrice, Order, ShoppingCart

# Register your models here.
admin.site.register(BasePrice)
admin.site.register(FoodType)
admin.site.register(Size)
admin.site.register(Topping)
admin.site.register(ToppingPrice)
admin.site.register(Order)
admin.site.register(ShoppingCart)
