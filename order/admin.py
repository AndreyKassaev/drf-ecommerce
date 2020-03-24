from django.contrib import admin
from .models import Order, Address


class OrderAdminPanel(admin.ModelAdmin):
    # readonly_fields = ('total_price', 'items', 'user')
    readonly_fields = ('cart', 'address',)
    list_display = ('id', 'is_payed', 'is_delivered',)

class AddressAdminPanel(admin.ModelAdmin):
    # readonly_fields = ('total_price', 'items', 'user')
    readonly_fields = ('customer', )
    list_display = ('id', 'email',)


    
admin.site.register(Order, OrderAdminPanel)
admin.site.register(Address, AddressAdminPanel)
