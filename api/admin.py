from django.contrib import admin
from .models import CustomUsers, RecipesCategory, ingredientsPerServing, Steps, RecipeList, ServeHistory

admin.site.register(CustomUsers)
admin.site.register(ingredientsPerServing)
admin.site.register(RecipesCategory)
admin.site.register(Steps)
admin.site.register(RecipeList)
admin.site.register(ServeHistory)

