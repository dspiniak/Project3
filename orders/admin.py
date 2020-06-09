from django.contrib import admin

from .models import BasePrice, FoodType, Size, Topping, ToppingPrice

# Register your models here.
admin.site.register(BasePrice)
admin.site.register(FoodType)
admin.site.register(Size)
admin.site.register(Topping)
admin.site.register(ToppingPrice)
