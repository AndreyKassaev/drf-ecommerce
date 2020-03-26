from rest_framework import serializers
from .models import Author

class AuthorSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField('get_image')

    def get_image(self, obj):
        return obj.image.url

    class Meta:
        model = Author
        fields = ['id','image', 'name', 'bio']


class UpdateProfileSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField('get_image')

    def get_image(self, obj):
        return obj.image.url

    class Meta:
        model = Author
        fields = '__all__'

class BecomeAnAuthorSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    image = serializers.SerializerMethodField('get_image')

    def get_image(self, obj):
        return obj.image.url

    class Meta:
        model = Author
        fields = ['image', 'user', 'name', 'bio']
        