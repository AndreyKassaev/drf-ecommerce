from rest_framework import serializers

from .models import CartItem, Cart
from product.serializers import ProductListSerializer
from product.models import Product

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(Product.objects.all(), many=True)
    class Meta:
        model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    items = serializers.StringRelatedField(many=True)
    class Meta:
        model = Cart
        fields = ['items', 'is_active', 'is_payed', 'date_created', 'total_price', 'total_items']
