from django.urls import path
from . import views
from .views import RegisterUser, CustomAuthToken, User_logout, UserRecordView, SearchRecipeListView
urlpatterns = [
    path('', views.getRoutes),
    path('auth/register', RegisterUser.as_view()),
    path('auth/login', CustomAuthToken.as_view()),
    path('auth/logout', views.User_logout),
    path('recipe-categories', views.getAllRecipeCategory),
    path('recipe-categories/<int:pk>', views.CategoryAction),
    path('recipes', views.getListRecipes),
    path('recipes/<str:pk>', views.getDetailRecipes),
    path('search/recipes', SearchRecipeListView.as_view()),
    path('user/', UserRecordView.as_view(), name='users'),
]