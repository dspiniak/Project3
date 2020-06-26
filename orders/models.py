from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topping(models.Model):
    topping = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.topping}"

    def natural_key(self):
        return (self.topping)


class Size(models.Model):
    size = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.id}: {self.size}"

    def natural_key(self):
        return (self.size)


class FoodType(models.Model):
    category = models.CharField(max_length=20)
    base = models.CharField(max_length=30)
    toppings = models.ManyToManyField(Topping, blank=True)
    size = models.ManyToManyField(Size)

    def __str__(self):
        return f"{self.id}: {self.category}-{self.base}"

    def natural_key(self):
        return (self.category, self.base)


class BasePrice(models.Model):
    food = models.ForeignKey(FoodType, on_delete=models.CASCADE, related_name="base_price")
    size = models.ForeignKey(Size, on_delete=models.CASCADE, default=1)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.size}: ${self.price}"


class ToppingPrice(models.Model):
    food = models.ManyToManyField(FoodType, related_name="topping_price")
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
    order_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        # toppings_string = ", ".join(map(str,self.toppings))
        return f"order #{self.username} ordered: {self.food_type}, size {self.size}, {self.toppings} at ${self.order_price}"


class ShoppingCart(models.Model):
    status_choices = (
        ("unconfirmed", "unconfirmed"),
        ("pending", "pending"),
        ("complete", "complete")
    )

    username = models.ForeignKey(User, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(
        max_length = 20,
        choices = status_choices,
        default = '1'
        )

    def __str__(self):
        return f"{self.username} has orders. Status {self.status}. Total is ${self.total_price}"
