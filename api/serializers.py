from pyexpat import model
from django.contrib.auth import get_user_model


from rest_framework.validators import UniqueTogetherValidator
from rest_framework.serializers import ModelSerializer
from .models import RecipesCategory, RecipeList, Steps, ingredientsPerServing, ServeHistory
from rest_framework import serializers
User = get_user_model()
class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "password",

        ]
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user


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
        
class CreateIngredientsPerServingSerializer(ModelSerializer):
    class Meta:
        model = ingredientsPerServing
        fields = (
            'item',
            'unit',
            'value'

        )


class CreateStepsSerializer(ModelSerializer):
    class Meta:
        model = Steps
        fields = (
            'stepOrder',
            'description',

        )
    
class CreateRecipesSerializer(ModelSerializer):
    class Meta:
        model = RecipeList
        fields = (
            'name',
            'recipeCategoryId',
            'image',
            'nServing',
            'ingredientsPerServing',
            # 'steps'

        )
class RecipesDetailSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = RecipeList
        fields = (
            'id',
            'name',
            'recipeCategoryId',
            'image',
            'nServing',
            'nReactionLike',
            'nReactionNeutral',
            'nReactionDislike',
            'created_at',
            'updatedAt',

        )
    
class SearchRecipesSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = RecipeList
        fields = (
            'id',
            'name'

        )

class ServeHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServeHistory
        fields = (
            'id',
            'recipeId',
            'userId'
        )