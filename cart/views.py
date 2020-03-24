from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from cart.models import Cart, CartItem
from product.models import Product
from user_app.models import Customer
from .serializers import CartSerializer

import uuid

class ListAllCarts(ListAPIView):
    serializer_class = CartSerializer
    def get_queryset(self):
        user = self.request.user.customer
        carts = user.cart.all()
        return carts



@api_view(["GET"])
def get_cart(request):
    """Return Cart Instance"""
      # user instance
    try:
        try:
            user = request.user.customer
        # user is anonymous
        except:
            sid = request.META['HTTP_SESSIONID']
            user = Customer.objects.get(session=sid)
    except:
        return Response({'err_msg':'Anonymous Request'})

    try:
        cart = user.cart.get(is_active=True)
        serializer = CartSerializer(cart)
        return Response({'cart':serializer.data})
    # user hasn't active cart
    except:
        return Response({'err_msg':'No Active Cart'})

@api_view(["GET"])
def cart_items_quantity(request):
    """Return Quantity of Items inside Cart"""
     # user instance
    try:
        try:
            user = request.user.customer
        # user is anonymous
        except:
            sid = request.META['HTTP_SESSIONID']
            user = Customer.objects.get(session=sid)
    except:
        return Response({'err_msg':'Anonymous Request'})

    try:
        cart = user.cart.get(is_active=True)
        total_items = cart.total_items
        return Response({'msg':total_items})
    # user hasn't active cart
    except:
        return Response({'err_msg':'No Active Cart'})

@api_view(["GET"])
def remove_item(request, product_id):
    """Remove Item From Cart"""

    # validate params
    try:
        product_id = int(product_id)
        product = Product.objects.get(id=product_id)
    # product doesn't exists
    except:
        return Response({'err_msg':"Product Doesn't Exists"})

     # user instance
    try:
        try:
            user = request.user.customer
        # user is anonymous
        except:
            sid = request.META['HTTP_SESSIONID']
            user = Customer.objects.get(session=sid)
    except:
        return Response({'err_msg':'Anonymous Request'})

    try:
        cart = user.cart.get(is_active=True)
        item = cart.items.get(product__id=product_id)
        item.delete()
        return Response({'msg':'Item Removed From Cart'})
    # user hasn't active cart
    except:
        return Response({'err_msg':'No Active Cart'})

@api_view(["GET"])
def cart_total_price(request):
    """Return Cart's total price """
     # user instance
    try:
        try:
            user = request.user.customer
        # user is anonymous
        except:
            sid = request.META['HTTP_SESSIONID']
            user = Customer.objects.get(session=sid)
    except:
        return Response({'err_msg':'Anonymous Request'})

    try:
        cart = user.cart.get(is_active=True)
        total_price = cart.total_price
        return Response({'price':total_price})
    # user hasn't active cart
    except:
        return Response({'err_msg':'No Active Cart'})

@api_view(['GET'])
def increase_quantity(request, product_id):
    """Increase quantity of cart's product or add product to cart"""
    
    # validate params
    try:
        product_id = int(product_id)
        product = Product.objects.get(id=product_id)
    # product doesn't exists
    except:
        return Response({'err_msg':"Product Doesn't Exists"})

    # user instance
    try:
        try:
            user = request.user.customer
        # user is anonymous
        except:
            sid = request.META['HTTP_SESSIONID']
            user = Customer.objects.get(session=sid)
    except:
        sid = str(uuid.uuid4())
        custom_header = {'sessionid':sid}

        user = Customer.objects.create(session=sid)
        cart_item = CartItem.objects.create(product=product)
        cart = Cart.objects.create(user=user)
        cart.items.add(cart_item)
        cart.save()

        return Response({
            'msg':f'{cart_item} Added To New Cart New Session',
            'sid':f'{sid}'
            },
             headers=custom_header)

    # user has active cart
    try:
        # user's cart already has product
        try:
            cart = user.cart.get(is_active=True)
            cart_item = cart.items.get(product__id=product_id)
            cart_item.quantity += 1
            cart_item.save()
            return Response({'msg':f'{cart_item}'})
        # user's cart hasn't product
        except:
            cart_item = CartItem.objects.create(product=product)
            cart.items.add(cart_item)
            return Response({'msg':f'{cart_item}'})
    # user hasn't active cart
    except:
        cart_item = CartItem.objects.create(product=product)
        cart = Cart.objects.create(user=user)
        cart.items.add(cart_item)
        cart.save()
        return Response({'msg':f'{cart_item} Added To New Cart'})


@api_view(['GET'])
def decrease_quantity(request, product_id):
    """Decrease quantity of cart's product or remove product from cart"""

    # validate params
    try:
        product_id = int(product_id)
        product = Product.objects.get(id=product_id)
    # product doesn't exists
    except:
        return Response({'err_msg':"Product Doesn't Exists"})

    # user instance
    try:
        try:
            user = request.user.customer
        # user is anonymous
        except:
            sid = request.META['HTTP_SESSIONID']
            user = Customer.objects.get(session=sid)
    except:
        return Response({'err_msg':'Anonymous Request'})

    # user has active cart
    try:
        cart = user.cart.get(is_active=True)
        # user's cart has product
        try:
            cart_item = cart.items.get(product__id=product_id)
            if cart_item.quantity > 0:
                cart_item.quantity -= 1
                cart_item.save()
                return Response({'msg':f'{cart_item}'})
            else:
                cart_item.delete()
                return Response({'msg':'Product Removed From Cart'})
        # user's cart hasn't product
        except:
            return Response({'err_msg':'No Such Product Inside Cart'})
    # user hasn't active cart
    except:
        return Response({'err_msg':'No Active Cart'})

@api_view(['GET'])
def change_quantity(request, cart_item_id, quantity):
    """Change product's quantity"""
    
    # validate params
    try:
        cart_item_id = int(cart_item_id)
        quantity = int(quantity)
        quantity >= 0
    except:
        return Response({'err_msg':'Wrong Quantity'})

    # user instance
    try:
        try:
            user = request.user.customer
        # user is anonymous
        except:
            sid = request.META['HTTP_SESSIONID']
            user = Customer.objects.get(session=sid)
    except:
        return Response({'err_msg':'Anonymous Request'})

    # item quantity
    try:
        cart = user.cart.get(is_active=True)
        cart_item = cart.items.get(id=cart_item_id)
        cart_item.quantity = quantity
        cart_item.save()
        return Response({'msg':f'changed {cart_item}'})
    except:
        return Response({'err_msg':'No Active Cart or Wrong Item'})


@api_view(['GET'])
def clean_cart(request, cart_id):
    """Remove all products from cart"""
    
    # validate params
    try:
        cart_id = int(cart_id)
    except:
        return Response({'err_msg':'Wrong CartId'})

    # user instance
    try:
        try:
            user = request.user.customer
        # user is anonymous
        except:
            sid = request.META['HTTP_SESSIONID']
            user = Customer.objects.get(session=sid)
    except:
        return Response({'err_msg':'Anonymous Request'})

    # clean cart
    try:
        cart = user.cart.get(id=cart_id)
        cart.items.clear()
        return Response({'msg':'Cart Cleared'})
    except:
        return Response({'err_msg':'Cart Not Found'})