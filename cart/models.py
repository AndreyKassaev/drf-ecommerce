from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import F, Sum

from product.models import Product


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(0)], default=1)

    def __str__(self):
        return f"{self.product.id} {self.product.price} {self.quantity} of {self.product.title}"



class Cart(models.Model):
    user = models.ForeignKey('user_app.Customer', on_delete=models.CASCADE, related_name='cart')
    items = models.ManyToManyField(CartItem, related_name='cart')
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_payed = models.BooleanField(default=False)
    
    # user able have only one active cart
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user'], condition=models.Q(is_active=True), name='unique_field')
        ]


    @property
    def total_price(self):
        total = self.items.aggregate(total_price=Sum(F('quantity') * F('product__price')))['total_price']
        if not self.discount:
            return total
        return total - ((total*self.discount)/100) 

    @property
    def total_items(self):
        total = self.items.aggregate(total_items=Sum(F('quantity') * 1))['total_items']
        return total 

    def __str__(self):
        return f'cart id: {self.id} of {self.user}'