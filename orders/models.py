from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topping(models.Model):
    topping = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.topping}"


class Size(models.Model):
    size = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.size}"


class FoodType(models.Model):
    category = models.CharField(max_length=20)
    base = models.CharField(max_length=30)
    toppings = models.ManyToManyField(Topping, blank=True)
    size = models.ManyToManyField(Size)

    def __str__(self):
        return f"{self.id}: {self.category}-{self.base}"


class BasePrice(models.Model):
    food = models.ForeignKey(FoodType, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, default=1)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"${self.price}"


class ToppingPrice(models.Model):
    food = models.ManyToManyField(FoodType)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
    topping_num = models.IntegerField()
    price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"${self.price}"


class Order(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    food_type = models.ForeignKey(FoodType, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    toppings = models.ManyToManyField(Topping, blank=True)
    base_price = models.ForeignKey(BasePrice, on_delete=models.CASCADE)
    topping_price = models.ForeignKey(ToppingPrice, on_delete=models.CASCADE)

    def __str__(self):
        return f"order #{self.id} - {self.username} ordered: {self.food_type}, size {self.size}, topping {self.topping}, at ${self.base_price} + ${self.base_price}"
