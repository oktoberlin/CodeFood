from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db import models
import string
import random
class MyAccountManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_active=True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

class CustomUsers(AbstractBaseUser):
    username= models.CharField(max_length=30,unique=True, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_teacher = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_super_teacher = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    

    def has_perm(self, perm, obj=None): return self.is_superuser

    def has_module_perms(self, app_label): return self.is_superuser

class RecipesCategory(models.Model):
    name = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name



class RecipeList(models.Model):
    name = models.TextField()
    recipeCategoryId =  models.ForeignKey(RecipesCategory, related_name='recipeCategoryId',on_delete=models.SET_NULL, null=True, blank=False)
    image = models.ImageField(upload_to='images',default='test.jpg',null=True, blank=True)
    nServing = models.IntegerField(default=1,null=False, blank=False)
    nReactionLike = models.IntegerField(default=0,null=False, blank=False)
    nReactionNeutral = models.IntegerField(default=0,null=False, blank=False)
    nReactionDislike = models.IntegerField(default=0,null=False, blank=False)
    createdAt=  models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(default=datetime.now)
    
    def __str__(self):
        return self.name
   
    class Meta:
        ordering = ['createdAt']

class Steps(models.Model):
    recipeListId = models.ForeignKey(RecipeList,related_name='steps',on_delete=models.SET_NULL, null=True, blank=False)
    stepOrder = models.IntegerField(default=0,null=False, blank=False)
    description = models.CharField(max_length=100)
    done = models.BooleanField(default=False)

    def __str__(self):
        return str(self.stepOrder)


class ingredientsPerServing(models.Model):
    recipeListId = models.ForeignKey(RecipeList,related_name='ingredientsPerServing',on_delete=models.SET_NULL, null=True, blank=False)
    item = models.TextField()
    unit = models.CharField(max_length=50)
    value = models.IntegerField(default=0,null=False, blank=False)

    def __str__(self):
        return self.item

def id_generator(size=4, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
class ServeHistory(models.Model):
    
    id = models.CharField(max_length=4, unique=True, primary_key=True, default=id_generator(), editable=False)
    recipeId = models.ForeignKey(RecipeList,related_name='serveHistory',on_delete=models.SET_NULL, null=True, blank=False)
    userId = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='userId',on_delete=models.SET_NULL, null=True, blank=False)
    def __str__(self):
        return self.id
