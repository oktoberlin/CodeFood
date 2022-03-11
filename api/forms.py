from django import forms
from .models import ingredientsPerServing

class ingredientsPerServingForm(forms.ModelForm):
    class Meta:
        model = ingredientsPerServing
        fields = '__all__'
