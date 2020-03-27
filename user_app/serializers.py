from rest_framework import serializers
from .models import Author

class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ['id','image', 'name', 'bio']


class UpdateProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = '__all__'

class BecomeAnAuthorSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Author
        fields = ['image', 'user', 'name', 'bio']
        
