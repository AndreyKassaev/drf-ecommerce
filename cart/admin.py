from django.contrib import admin
from .models import CartItem, Cart


class CartItemAdminPanel(admin.ModelAdmin):
    # readonly_fields = ('product','quantity')
    list_display = ('id','product','quantity')
    
class CartAdminPanel(admin.ModelAdmin):
    # readonly_fields = ('total_price', 'items', 'user')
    readonly_fields = ('total_price', 'total_items')
    list_display = ('id','user', 'total_price', 'is_active')


    
admin.site.register(CartItem, CartItemAdminPanel)
admin.site.register(Cart, CartAdminPanel)
