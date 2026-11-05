from django import forms
from .models import FoodItem


class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = [
            'name',
            'description',
            'price',
            'image',
            'is_available',
        ]