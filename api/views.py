import base64
from .serializers import RegistrationSerializer, RecipesCategorySerializer, RecipesListSerializer, CreateRecipesSerializer, CreateStepsSerializer, ListStepsSerializer, RecipesDetailSerializer, UserSerializer, CreateIngredientsPerServingSerializer, SearchRecipesSerializer, ServeHistorySerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics, filters
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model, logout
from .models import RecipesCategory, RecipeList, Steps, ingredientsPerServing, ServeHistory
from rest_framework.parsers import FileUploadParser, MultiPartParser
User = get_user_model()

@permission_classes([AllowAny])
class RegisterUser(APIView):
    def post(self, request):
        if request.data['username'] == '':
            return Response({"success": False,"message":"username is required",})
        elif request.data['password'] == '':
            return Response({"success": False,"message":"password is required",})
        elif len(request.data['password']) < 6:
            return Response({"success": False,"message":"password minimum 6 characters",})
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
        
            serializer.save()
            username = serializer.data['username']
            user = User.objects.get(username=username)
            
            token, _ = Token.objects.get_or_create(user=user)
            
            return Response({"success": True,"message":"Success","data":{"id":user.id,"username":user.username}})
        else:
            return Response({"success": False,"message":"username "+request.data['username']+" already registered",})
class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        data=request.data
        if request.data['username'] == '':
            return Response({"success": False,"message":"username is required",})
        elif request.data['password'] == '':
            return Response({"success": False,"message":"password is required",})

        
        serializer = self.serializer_class(data=data,
                                           context={'request': request})
        
        if not serializer.is_valid():
            return Response({"success": False,"message":"Invalid username or Password"})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        token, created = Token.objects.get_or_create(user=user)
        return Response({"success": True,"message":"Success","data":{"token":token.key}})

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def User_logout(request):

    request.user.auth_token.delete()

    logout(request)

    return Response('User Logged out successfully')
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
@permission_classes([AllowAny])
def getRoutes(request):
    routes = [
        {
            'Register User': '/auth/register',
            'Login User': '/auth/login',
            'Recipe Categories List': '/recipe-categories',
            'Recipe Category Detail': '/recipe-categories/<int:pk>',
            'Recipes List': '/recipes',
            'Recipes Detail': '/recipes/<str:pk>',
            'Recipes Detail Step': '/recipes/<str:pk>/steps',
            'Serve History List': '/serve-histories',
            'Serve History Detail Step Done': '/serve-histories/<str:name>/done-step',
            'Search Recipes': '/search/recipes'

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
        recipes = RecipeList.objects.create(
            name=data['name'],
            recipeCategoryId=RecipesCategory.objects.get(id=data['recipeCategoryId']),
            image=data['image'],
            nServing=data['nServing'],
        )
        recipesSerializer = CreateRecipesSerializer(recipes)
        dataJson= recipesSerializer.data

        for item in data['ingredientsPerServing']:
            ingredientsPerServing.objects.create(
                recipeListId=RecipeList.objects.get(id=recipes.id),
                item=item['item'],
                unit=item['unit'],
                value=item['value']
            )
        ingredientsPerServingObjects = ingredientsPerServing.objects.filter(recipeListId=recipes.id)
        ingredientsPerServingSerializer=CreateIngredientsPerServingSerializer(ingredientsPerServingObjects, many=True)
        dataJson['ingredientsPerServing'] = ingredientsPerServingSerializer.data
        for item in data['steps']:
            Steps.objects.create(
                recipeListId=RecipeList.objects.get(id=recipes.id),
                stepOrder=item['stepOrder'],
                description=item['description'],
            )
        stepsObjects = Steps.objects.filter(recipeListId=recipes.id)
        stepSerializer = CreateStepsSerializer(stepsObjects, many=True)
        dataJson['steps'] = stepSerializer.data
        return Response({"success": True,"message":"Success","data":dataJson})

@api_view(['GET','PUT', 'DELETE'])
def getDetailRecipes(request, pk):

    try:
        recipes = RecipeList.objects.get(id=pk)
    except RecipeList.DoesNotExist:
        return Response({"success": False,"message":"Recipe with id "+ str(pk)+" not found",})
    
    if request.method == 'GET':
        serializer = RecipesDetailSerializer(recipes, many=False)
        data = serializer.data

        ingredientsPerServingObjects=ingredientsPerServing.objects.filter(recipeListId=recipes.id)
        # if request.GET.get('nServing') > 1:

        ingredientsPerServingSerializer = CreateIngredientsPerServingSerializer(ingredientsPerServingObjects, many=True)
        data['ingredientsPerServing'] = ingredientsPerServingSerializer.data

        stepsObjects = Steps.objects.filter(recipeListId=recipes.id)
        stepsSerializer = CreateStepsSerializer(stepsObjects, many=True)
        data['steps'] = stepsSerializer.data

        recipeCategory = RecipesCategory.objects.get(pk=data['recipeCategoryId'])
        recipeCategorySerializer = RecipesCategorySerializer(recipeCategory)
        data['recipeCategory'] = recipeCategorySerializer.data
        

        # data['ingredientsPerServing'] = listIngredientsPerServing
        return Response(
            {
                "success": True,
                "message":"Success",
                "data": data
            })

    elif request.method == 'PUT':
        if request.data['name'] == '':
            return Response({"success": False,"message":"name is required",})
        elif type(request.data['recipeCategoryId']) != int:
            return Response({"success": False,"message":"recipeCategoryId is required and must be integer",})
        serializer = RecipesDetailSerializer(recipes, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            dataJson=serializer.data
            ingredientsPerServingObjects=ingredientsPerServing.objects.filter(recipeListId=recipes.id)
            ingredientsPerServingSerializer = CreateIngredientsPerServingSerializer(ingredientsPerServingObjects, many=True)
            dataJson['ingredientsPerServing'] = ingredientsPerServingSerializer.data

            stepsObjects = Steps.objects.filter(recipeListId=recipes.id)
            stepsSerializer = CreateStepsSerializer(stepsObjects, many=True)
            dataJson['steps'] = stepsSerializer.data
            return Response({"success": True,"message":"Success","data":dataJson})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        recipes.delete()
        return Response({"success": True,"message": "Success","data": {}})

@api_view(['GET'])
def getListRecipesSteps(request, pk):
    if request.method == 'GET':
        recipesList = Steps.objects.filter(recipeListId=pk)
        serializer = CreateStepsSerializer(recipesList, many=True)
        data = serializer.data
        return Response(
            {
                "success": True,
                "message":"Success",
                "data": data
            })


@api_view(['GET','POST'])
def getListServeHistory(request):
    if request.user.is_authenticated:
    
        if request.method == 'GET':
            serveHistoryList = ServeHistory.objects.all()
            serveHistoryListCount = ServeHistory.objects.all().count()
            serveHistoryListSerializer = ServeHistorySerializer(serveHistoryList, many=True)
            data = serveHistoryListSerializer.data
            for i in range(len(data)):
                recipeData = RecipeList.objects.get(id=data[i]['recipeId'])
                data[i]['recipeName'] = recipeData.name
                data[i]['recipeCategoryName'] = recipeData.recipeCategoryId.name
                data[i]['recipeImage'] = recipeData.image.url

                stepData = Steps.objects.filter(recipeListId=data[i]['recipeId']).count()
                data[i]['nStep'] = stepData
                data[i]['createdAt'] = recipeData.createdAt
                data[i]['updatedAt'] = recipeData.updatedAt
                # nStepDone
            return Response(
                {
                    "success": True,
                    "message":"Success",
                    "data": {
                        "total": serveHistoryListCount,
                        "history": data
                    }
                })
        
        # Create Serve History
        elif request.method == 'POST':
            parser_class = (FileUploadParser, MultiPartParser,)
            data = request.data
            try:
                recipeData = RecipeList.objects.get(id=data['recipeId'])
            except RecipeList.DoesNotExist:
                return Response({"success": False,"message":"Recipe with id "+ str(data['recipeId'])+" not found",})
            
            if type(data['nServing']) != int:
                return Response({"success": False,"message":"nServing is required and must be integer",})
            elif type(data['recipeId']) != int:
                return Response({"success": False,"message":"recipeId is required and must be integer",})
            serveHistory = ServeHistory.objects.create(
                recipeId=RecipeList.objects.get(id=data['recipeId']),
                userId = User.objects.get(id=request.user.id)
            )
            
            serveHistorySerializer = ServeHistorySerializer(serveHistory)
            dataJson= serveHistorySerializer.data
            dataJson['nServing'] = data['nServing']
            dataJson['recipeName'] = recipeData.name
            dataJson['recipeCategoryName'] = recipeData.recipeCategoryId.name
            dataJson['recipeImage'] = recipeData.image.url

            stepData = Steps.objects.filter(recipeListId=data['recipeId'])
            stepDataSerializer = ListStepsSerializer(stepData, many=True)
            dataJson['steps'] = stepDataSerializer.data
            stepDataCount = Steps.objects.filter(recipeListId=data['recipeId']).count()
            
            dataJson['nStep'] = stepDataCount
            stepDoneCount = Steps.objects.filter(recipeListId=data['recipeId'],done=True).count()
            dataJson['nStepDone'] = stepDoneCount
            dataJson['createdAt'] = recipeData.createdAt
            dataJson['updatedAt'] = recipeData.updatedAt
            
            # nStepDone
            return Response(
                {
                    "success": True,
                    "message":"Success",
                    "data": {
                        "history": dataJson
                    }
                })
    else:
        return Response(
            {
                "success": True,
                "message":"Unauthorized",
            })
    

@api_view(['PUT'])
def updateStepDone(request, name):

    try:
        serveHistory = ServeHistory.objects.get(id=name)
    except ServeHistory.DoesNotExist:
        return Response({"success": False,"message":"Serve history with id "+ name+" not found",})
    
    
    if request.method == 'PUT':
        if request.data['stepOrder'] == '':
            return Response({"success": False,"message":"stepOrder is required",})
        # elif type(request.data['recipeCategoryId']) != int:
        #     return Response({"success": False,"message":"recipeCategoryId is required and must be integer",})
        serializer = ServeHistorySerializer(serveHistory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            dataJson=serializer.data
            
            stepsObjects = Steps.objects.filter(recipeListId=dataJson['recipeId'])

            stepsObjects[request.data['stepOrder']-1].done = True
            stepsObjects[request.data['stepOrder']-1].save()
            stepsSerializer = ListStepsSerializer(stepsObjects, many=True)
            dataJson['steps'] = stepsSerializer.data
            return Response({"success": True,"message":"Success","data":dataJson})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

@api_view(['GET'])
def SearchRecipes(request):
    
    if request.method == 'GET':
        print(request.GET.get('q', ''))
        recipesList = RecipeList.objects.get(name__icontains=request.GET.get('q', ''))
        serializer = SearchRecipesSerializer(recipesList)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True,"message":"Success","data":serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchRecipeListView(generics.ListAPIView):
    queryset = RecipeList.objects.all()
    serializer_class = SearchRecipesSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',]


