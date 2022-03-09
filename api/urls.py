from django.urls import path
from . import views
from .views import UserRecordView
urlpatterns = [
    path('', views.getRoutes),
    path('recipes/', views.getFoodLists),
    path('recipes/create/', views.createFood),
    path('recipes/<str:pk>/update/', views.updateFood),
    path('recipes/<str:pk>/delete/', views.deleteFood),
    path('recipes/<str:pk>/', views.getFood),
    path('user/', UserRecordView.as_view(), name='users'),
]