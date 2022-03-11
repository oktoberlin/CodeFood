from pyexpat import model
from django.contrib.auth import get_user_model


from rest_framework.validators import UniqueTogetherValidator
from rest_framework.serializers import ModelSerializer
from .models import RecipesCategory, RecipeList, Steps, ingredientsPerServing
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
        
class ingredientsPerServingSerializer(ModelSerializer):
    class Meta:
        model = ingredientsPerServing
        fields = '__all__'

class CreateRecipesSerializer(ModelSerializer):
    class Meta:
        model = RecipeList
        fields = (
            'name',
            'recipeCategoryId',
            'image',
            'nServing',
            'ingredientsPerServing',
            'steps'

        )
    def create(self, request, validated_data):
        data=request.data
        print(data)
        stepOrder = data['steps'][0]['stepOrder']
        description = data['steps'][0]['description']
        steps, created = Steps.objects.get_or_create(stepOrder=stepOrder, description=description)
        steps_instance = RecipeList.objects.create(**validated_data, name=data['name'],
            recipeCategoryId=RecipesCategory.objects.get(id=data['recipeCategoryId']),
            image=data['image'],
            nServing=data['nServing'],
            ingredientsPerServing=ingredientsPerServing.objects.get(id=data['ingredientsPerServing']),steps=steps)
        return steps_instance
class RecipesDetailSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = RecipeList
        fields = (
            'id',
            'name',
            'recipeCategoryId',
            'image',
            'nServing',
            'steps',
            'ingredientsPerServing',
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