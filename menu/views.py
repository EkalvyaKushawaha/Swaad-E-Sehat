from django.shortcuts import render, get_object_or_404
from .models import FoodItem, Category

def menu_list(request):
    categories = Category.objects.all()
    foods = FoodItem.objects.filter(is_available=True)
    q = request.GET.get('q')
    cat = request.GET.get('category')
    sort = request.GET.get('sort')

    if q:
        foods = foods.filter(name__icontains=q)
    if cat:
        foods = foods.filter(category_id=cat)
    if sort == 'low':
        foods = foods.order_by('price')
    elif sort == 'high':
        foods = foods.order_by('-price')

    return render(request, 'menu/menu_list.html', {'foods': foods, 'categories': categories})

def food_detail(request, pk):
    food = get_object_or_404(FoodItem, pk=pk)
    return render(request, 'menu/food_detail.html', {'food': food})
