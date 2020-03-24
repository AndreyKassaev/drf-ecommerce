from django.urls import path, include
from .views import (
    ListAllAuthors,
    SingleAuthor,
    ValidateEmail,
    BecomeAnAuthor,
    are_you_author,
    UpdateProfile
)


urlpatterns = [
    path('', include('django.contrib.auth.urls')), 
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('authors-list/', ListAllAuthors.as_view()),
    path('single-author/<name>/', SingleAuthor.as_view()),
    path('validate-email/<email>/', ValidateEmail),
    path('become-an-author/', BecomeAnAuthor.as_view()),
    path('are-you-author/', are_you_author),
    path('update-profile/<pk>', UpdateProfile.as_view())
]