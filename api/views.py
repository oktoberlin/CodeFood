from .serializers import RecipesCategorySerializer, RecipesListSerializer, CreateRecipesSerializer, RecipesDetailSerializer, UserSerializer, ingredientsPerServingSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User
from .models import RecipesCategory, RecipeList, Steps, ingredientsPerServing
from rest_framework.parsers import FileUploadParser, MultiPartParser

class UserRecordView(APIView):
    
    permission_classes = [IsAdminUser]

    def get(self, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "error": True,
                "error_msg": serializer.error_messages,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/recipes/create/'
        }
    ]

    return Response(routes)


@api_view(['GET','POST'])
def getAllRecipeCategory(request):
    if request.method == 'GET':
        snippets = RecipesCategory.objects.all()
        serializer = RecipesCategorySerializer(snippets, many=True)
        return Response({"success": True,"message":"Success","data":serializer.data})

    elif request.method == 'POST':
        if request.data['name'] == '':
            return Response({"success": False,"message":"name is required",})
        serializer = RecipesCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True,"message":"Success","data":serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['PUT', 'DELETE'])
def CategoryAction(request, pk):
    try:
        category = RecipesCategory.objects.get(pk=pk)
    except RecipesCategory.DoesNotExist:
        return Response({"success": False,"message":"Recipe Category with id "+ str(pk)+" not found",})

    if request.method == 'PUT':
        if request.data['name'] == '':
            return Response({"success": False,"message":"name is required",})
        serializer = RecipesCategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True,"message":"Success","data":serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        category.delete()
        return Response({"success": True,"message": "Success","data": {}})

@api_view(['GET','POST'])
def getListRecipes(request):
    recipesList = RecipeList.objects.all()
    recipesListCount = RecipeList.objects.all().count()
    serializer = RecipesListSerializer(recipesList, many=True)
    data = serializer.data

    if request.method == 'GET':
        for i in range(len(data)):
            
            recipeCategory = RecipesCategory.objects.get(pk=data[i]['recipeCategoryId'])
            recipeCategorySerializer = RecipesCategorySerializer(recipeCategory)
            data[i]['recipeCategory'] = recipeCategorySerializer.data
        return Response(
            {
                "success": True,
                "message":"Success",
                "data": {
                    "total": recipesListCount,
                    "recipes": data
                }
            })
    
    # Create Recipes
    elif request.method == 'POST':
        parser_class = (FileUploadParser, MultiPartParser,)
    
        data = request.data
        if data['name'] == '':
            return Response({"success": False,"message":"name is required",})
        elif type(data['recipeCategoryId']) != int:
            return Response({"success": False,"message":"recipeCategoryId is required and must be integer",})
        # recipes = RecipeList.objects.create(
        #     name=data['name'],
        #     recipeCategoryId=RecipesCategory.objects.get(id=data['recipeCategoryId']),
        #     image=data['image'],
        #     nServing=data['nServing'],
        #     ingredientsPerServing=ingredientsPerServing.objects.get(id=data['ingredientsPerServing']),
        #     # steps=data['steps'],
        # )
        # serializer = CreateRecipesSerializer(recipes, many=True)
        return Response({"success": True,"message":"Success","data":serializer.data})

@api_view(['GET','PUT', 'DELETE'])
def getDetailRecipes(request, pk):

    try:
        recipes = RecipeList.objects.get(id=pk)
    except RecipeList.DoesNotExist:
        return Response({"success": False,"message":"Recipe with id "+ str(pk)+" not found",})
    
    if request.method == 'GET':
        recipesListCount = RecipeList.objects.all().count()
        serializer = RecipesDetailSerializer(recipes, many=False)
        data = serializer.data

        listdata=[]
        
        recipeCategory = RecipesCategory.objects.get(pk=data['recipeCategoryId'])
        recipeCategorySerializer = RecipesCategorySerializer(recipeCategory)

        ingredientsPerServingData = 1
        ingredientsPerServingDataSerializer = ingredientsPerServingSerializer(ingredientsPerServingData)
        
        data['recipeCategory'] = recipeCategorySerializer.data
        listIngredientsPerServing = []
        # listIngredientsPerServing.append(ingredientsPerServingDataSerializer.data)
        data['ingredientsPerServing'] = listIngredientsPerServing
        listdata.append(data)
        return Response(
            {
                "success": True,
                "message":"Success",
                "data": {
                    "total": recipesListCount,
                    "recipes": listdata
                }
            })

    elif request.method == 'PUT':
        if request.data['name'] == '':
            return Response({"success": False,"message":"name is required",})
        elif type(request.data['recipeCategoryId']) != int:
            return Response({"success": False,"message":"recipeCategoryId is required and must be integer",})
        serializer = RecipesDetailSerializer(recipes, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True,"message":"Success","data":serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        recipes.delete()
        return Response({"success": True,"message": "Success","data": {}})
