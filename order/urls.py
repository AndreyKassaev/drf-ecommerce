from django.urls import path

from .views import  payment, create_order

urlpatterns = [
    path('payment/', payment),
    path('create-order/', create_order)
]