from django.shortcuts import render
from menu.models import FoodItem

def home(request):
    featured_foods = FoodItem.objects.filter(is_available=True, is_featured=True)[:6]
    return render(request, 'core/home.html', {'featured_foods': featured_foods})

def about(request):
    return render(request, 'core/about.html')

def developer(request):
    return render(request, 'core/developer.html')