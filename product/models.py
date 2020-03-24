from django.db import models
from django.core.validators import MinValueValidator 
from django.conf import settings

class ProductCategory(models.Model):
    image = models.ImageField(null=True)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=255, unique=True)
    price = models.IntegerField(validators=[MinValueValidator(0)]) 
    description = models.TextField(max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(blank=True, null=True)
    categories = models.ManyToManyField(ProductCategory, related_name='products')
    author = models.ForeignKey('user_app.Author', related_name='products', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title