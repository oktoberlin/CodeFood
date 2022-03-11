from django.urls import path
from . import views
from .views import UserRecordView
urlpatterns = [
    path('', views.getRoutes),
    path('recipe-categories', views.getAllRecipeCategory),
    path('recipe-categories/<int:pk>', views.CategoryAction),
    path('recipes', views.getListRecipes),
    path('recipes/create/', views.createRecipes),
    path('recipes/<str:pk>/update/', views.updateRecipes),
    path('recipes/<str:pk>/delete/', views.deleteRecipe),
    path('recipes/<int:pk>', views.getDetailRecipes),
    path('user/', UserRecordView.as_view(), name='users'),
]