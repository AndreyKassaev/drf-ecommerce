from django.urls import path

from .views import (
    increase_quantity,
    decrease_quantity,
    change_quantity,
    clean_cart,
    cart_items_quantity,
    get_cart,
    cart_total_price,
    remove_item,
    ListAllCarts
    )


urlpatterns = [
    path('add-to-cart/<product_id>/', increase_quantity),
    path('change-quantity/<cart_item_id>/<quantity>/', change_quantity),
    path('remove-from-cart/<product_id>/', decrease_quantity),
    path('clean-cart/<cart_id>/',clean_cart),
    path('cart-quantity/', cart_items_quantity),
    path('get-cart/', get_cart),
    path('cart-total-price/', cart_total_price),
    path('remove-item/<product_id>/', remove_item),
    path('payment-history/', ListAllCarts.as_view())
]