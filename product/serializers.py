from rest_framework import serializers
from .models import Product, ProductCategory
from django.db.models import Q


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'

class CreateProductSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Product
        # fields = ['title', 'description', 'price', 'image', 'author', 'categories']
        exclude = ['author', 'categories']
        
class UpdateProductSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Product
        fields = '__all__'

        

class ProductListSerializer(serializers.ModelSerializer):
    categories = ProductCategorySerializer(ProductCategory.objects.all() ,many=True)
    author = serializers.CharField(source='author.name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'image', 'author', 'categories', ]


        