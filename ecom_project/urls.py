from django.contrib import admin
from django.urls import path, include

from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.conf.urls.static import static
from django.conf import settings

@api_view(['GET',])
def send_email(request):
    subject='subject1'
    message = 'plain text'
    server_mail = 'django_smtp@mail.ru'
    to = 'medahe1694@webbamail.com'
    html = '<h1>h1 tag</h1>'

    send_mail(
        subject=subject,
        message=message,
        from_email=server_mail,
        recipient_list=['medahe1694@webbamail.com',],
        fail_silently=False,
        html_message=html
    )
    return Response({'ok'})

urlpatterns = [
    path('test/', send_email),

    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('user_app.urls')),
    path('api/v1/product/', include('product.urls')),
    path('api/v1/cart/', include('cart.urls')),
    path('api/v1/order/', include('order.urls'))
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
