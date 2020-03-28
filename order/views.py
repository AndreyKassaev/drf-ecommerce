from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.mail import send_mail

from .models import Address, Order
from user_app.models import Customer
from django.conf import settings
# 1. user fill order form ---> recieve braintree token
# 2. user choose payments methods
# 3. braintree form
# 4.1 if resilt.is_success == True send email, redirect to main page and show success message
# 4.2 if resilt.is_success == False, redirect to order page and show fail message
import braintree
import os

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=os.getenv("MERCHANT_ID"),
        public_key=os.getenv("PUBLIC_KEY"),
        private_key=os.getenv("PRIVATE_KEY")
    )
)
@api_view(['POST',])
def create_order(request):
    """Create Order and Send Braintree Token Back"""

     # user instance
    try:
        try:
            user = request.user.customer
        # user is anonymous
        except:
            sid = request.META['HTTP_SESSIONID']
            user = Customer.objects.get(session=sid)
    except:
        return Response({'msg':'Anonymous Request'})

    # cart instance
    try:
        cart = user.cart.get(is_active=True)
    # user hasn't active cart
    except:
        return Response({'msg':'No Active Cart'})

    # create order
    try:

        data = request.data
        
        address = Address.objects.create(
            email=data['email'],
            country=data['country'],
            city=data['city'],
            street=data['street'],
            building=data['building'],
            apartment=data['apartment'],
            customer=user
            )

        order = Order.objects.create(
            cart=cart,
            address=address
        )
        order_id = order.id
    

        client_token = gateway.client_token.generate()
        
        return Response({'msg':'Order Created', 'client_token':client_token, 'order_id':order_id})

    except:

        return Response({'msg':'Order Not Created'})

    


@api_view(['POST'])
def payment(request):
    """Braintree transaction"""

    try:
        nonce = request.data['nonce']
        order_id = request.data['order_id']

        order = Order.objects.get(id=order_id)
        amount = order.cart.total_price
        email = order.address.email
        result = gateway.transaction.sale({
            "amount": amount,
            "payment_method_nonce": nonce,
            "options": {
                "submit_for_settlement": True
            }
        })
        if result.is_success:
            order.cart.is_active = False
            order.cart.is_payed = True
            order.cart.save()

            order.is_payed = True
            order.save()
            total_price = order.cart.total_price

            email_data = f'Order Is Payed, Total Price: {total_price} $'
            try:
                send_mail(
                    'Order',
                    email_data,
                    os.getenv('EMAIL_HOST_USER'),
                    [email,],
                    fail_silently=True
                    )
            except:
                return Response({'msg':'Payment Done But Email Not Send'})

            return Response({'msg':'Payment Done Check Your Email Inbox'})
        else: 
            return Response({'msg':'Payment Failed'})
    except:
        return Response({'msg':'Ooops...'})
