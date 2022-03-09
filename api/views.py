from .serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User
from .serializers import ListFoodSerializer
from .models import ListFood
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

@api_view(['GET'])
def getFoodLists(request):
    foodList = ListFood.objects.all()

    serializer = ListFoodSerializer(foodList, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getFood(request, pk):
    food = ListFood.objects.get(id=pk)

    serializer = ListFoodSerializer(food, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def createFood(request):
    parser_class = (FileUploadParser, MultiPartParser,)
    
    data = request.data
    #images = request.FILES.getlist(data['imagePaths'])
    #for image in images:
    note = ListFood.objects.create(
        
        name=data['name'],
        thumbnail=data['thumbnail'],
        category=data['category'],
        satisfied_count = data['satisfied_count'],
        createdTime=data['createdTime']
        
    )
    serializer = ListFoodSerializer(note, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
def updateFood(request, pk):
    data = request.data
    note = ListFood.objects.get(id=pk)
    serializer = ListFoodSerializer(note, data=data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def deleteFood(request,pk):
    note = ListFood.objects.get(id=pk)
    note.delete()
    return Response('Food was deleted')