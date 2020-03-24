from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model

from .models import Author
from .serializers import AuthorSerializer, BecomeAnAuthorSerializer, UpdateProfileSerializer
from .pagination import AuthorPagination

class BecomeAnAuthor(CreateAPIView):
    queryset = Author.objects.all()
    serializer_class = BecomeAnAuthorSerializer
    permission_classes = [IsAuthenticated, ]

class ListAllAuthors(ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    pagination_class = AuthorPagination

class SingleAuthor(RetrieveAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_field= 'name'

class UpdateProfile(UpdateAPIView):
    queryset = Author.objects.all()
    serializer_class = UpdateProfileSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        user = self.request.user.id
        qs = Author.objects.filter(user__id=user)
        return qs

    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)



@api_view(["GET"])
def are_you_author(request):
    try:
        author = request.user.author
        serializer = AuthorSerializer(author)
        return Response(serializer.data)
    except:
        return Response(False)

@api_view(["GET"])
def ValidateEmail(request, email):
    user = get_user_model()
    try:
        user_email = user.objects.get(email=email)
        return Response(True)
    except:
        return Response(False)

         

