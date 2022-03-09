from django.contrib.auth.models import User
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.serializers import ModelSerializer
from .models import ListFood

class UserSerializer(ModelSerializer):

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'password',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username',]
            )
        ]

class ListFoodSerializer(ModelSerializer):
    class Meta:
        model = ListFood
        fields = '__all__'