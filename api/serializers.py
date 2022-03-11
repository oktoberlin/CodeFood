from django.contrib.auth.models import User
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.serializers import ModelSerializer
from .models import RecipesCategory, RecipeList, ingredientsPerServing
from rest_framework import serializers
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

class RecipesCategorySerializer(ModelSerializer):
    class Meta:
        model = RecipesCategory
        fields = '__all__'
class RecipesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeList
        fields = (
            'id',
            'name',
            'recipeCategoryId',
            'image',
            'nReactionLike',
            'nReactionNeutral',
            'nReactionDislike',
            'created_at',
            'updatedAt',

        )
        
class ingredientsPerServingSerializer(ModelSerializer):
    class Meta:
        model = ingredientsPerServing
        fields = '__all__'
class RecipesDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeList
        fields = (
            'id',
            'name',
            'recipeCategoryId',
            'image',
            'nServing',
            'ingredientsPerServing',
            'nReactionLike',
            'nReactionNeutral',
            'nReactionDislike',
            'created_at',
            'updatedAt',

        )
        
