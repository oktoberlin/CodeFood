from django.db import models


class FoodCategory(models.Model):
    name = name = models.TextField()

    def __str__(self):
        return self.name
class ListFood(models.Model):
    name = models.TextField()
    thumbnail = models.ImageField(upload_to='images',default='test.jpg',null=False, blank=False)
    category =  models.ForeignKey(FoodCategory, on_delete=models.SET_NULL, null=True, blank=False)
    satisfied_count = models.IntegerField(null=False, blank=False)
    created_at=  models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['created_at']