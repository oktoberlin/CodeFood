from django.urls import path
from . import views
from .views import UserRecordView
urlpatterns = [
    path('', views.getRoutes),
    path('recipe-categories', views.getAllRecipeCategory),
    path('recipe-categories/<int:pk>', views.CategoryAction),
    path('recipes', views.getListRecipes),
    path('recipes/<str:pk>', views.getDetailRecipes),
    path('user/', UserRecordView.as_view(), name='users'),
]