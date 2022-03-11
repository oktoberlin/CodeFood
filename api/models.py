from datetime import datetime
from django.db import models


class RecipesCategory(models.Model):
    # id = models.IntegerField(primary_key=True)
    name = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name
    
    @property
    def my_field(self):
        return self.name
class ingredientsPerServing(models.Model):
    item = models.TextField()
    unit = models.TextField()
    value = models.IntegerField(default=0,null=False, blank=False)

    def __str__(self):
        return self.item

class Steps(models.Model):
    stepOrder = models.IntegerField(default=0,null=False, blank=False)
    description = models.CharField(max_length=100)
    

    def __str__(self):
        return self.description
class RecipeList(models.Model):
    name = models.TextField()
    recipeCategoryId =  models.ForeignKey(RecipesCategory, related_name='category_id',on_delete=models.SET_NULL, null=True, blank=False)
    image = models.ImageField(upload_to='images',default='test.jpg',null=False, blank=False)
    nServing = models.IntegerField(default=1,null=False, blank=False)
    ingredientsPerServing = models.ForeignKey(ingredientsPerServing,related_name='ingredientsPerServing',on_delete=models.SET_NULL, null=True, blank=False)
    steps = models.ForeignKey(Steps,related_name='steps',on_delete=models.SET_NULL, null=True, blank=False)
    nReactionLike = models.IntegerField(default=0,null=False, blank=False)
    nReactionNeutral = models.IntegerField(default=0,null=False, blank=False)
    nReactionDislike = models.IntegerField(default=0,null=False, blank=False)
    created_at=  models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(default=datetime.now)
    
    def __str__(self):
        return self.name
   
    class Meta:
        ordering = ['created_at']