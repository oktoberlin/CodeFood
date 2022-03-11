from django.contrib import admin
from .models import RecipesCategory, ingredientsPerServing, Steps, RecipeList

admin.site.register(ingredientsPerServing)
admin.site.register(RecipesCategory)
admin.site.register(Steps)
admin.site.register(RecipeList)

