from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in

from .managers import CustomUserManager
from cart.models import Cart

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='customer') 
    session = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        if not self.user:
            return f'Anonymous user with session id: {self.session}'
        return self.user.email


class Author(models.Model):
    image = models.ImageField(null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name="author")
    name = models.CharField(max_length=255)
    bio = models.TextField(max_length=1000)

    def __str__(self):
        return self.name


def create_customer(sender, **kwargs):
    """Bind every newly created User with Customer"""
    if kwargs['created']:
        customer = Customer.objects.create(user=kwargs['instance'])
        Cart.objects.create(user=customer)


post_save.connect(create_customer, sender=User)




def header_handler(user=None, request=None):
    """Custom signal"""
    if user and request:
        user_logged_in.send(sender=user.__class__, request=request, user=user)

def login_handler(sender, user, request, **kwargs):
    """If user during registration or login process
    has header 'sessionid', cart bound to 'sessionid'
    become a cart of logged user
    """
    #Is there 'sessionid' header?
    try:
        sid = request.META['HTTP_SESSIONID']
        session_user = Customer.objects.get(session=sid)
        session_user_cart = session_user.cart.first()
        print('cart found')
        logged_user = user.customer
        print('customer found')
        # Does Logged In user has active cart?
        try:
            active_cart = logged_user.cart.get(is_active=True)
            active_cart.is_active = False
            active_cart.save()
            logged_user.cart.add(session_user_cart)
            print('logged user added new cactive cart')
        
        # No active cart?
        except:
            logged_user.cart.add(session_user_cart)
            print('logged user got new cart')

    except:
        print('failed')
        pass

user_logged_in.connect(login_handler)