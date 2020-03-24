from django.db import models
from django.core.validators import MinValueValidator

from cart.models import Cart
from user_app.models import Customer


class Address(models.Model):
    email = models.EmailField()
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    building = models.IntegerField(validators=[MinValueValidator(1)])
    apartment = models.IntegerField(validators=[MinValueValidator(1)])
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return f'address of {self.email}'

class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='order')
    address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='address')
    is_payed = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)

    def __str__(self):
        return f'order with cart id {self.cart.id}'