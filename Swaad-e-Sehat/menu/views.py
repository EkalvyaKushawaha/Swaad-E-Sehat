from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FoodItem
from .forms import FoodItemForm


@login_required(login_url='custom_admin_login')
def add_food(request):
    if not request.user.is_staff:
        return redirect('custom_admin_login')

    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Food item added successfully.')
            return redirect('admin_dashboard')
    else:
        form = FoodItemForm()

    return render(request, 'menu/food_form.html', {
        'form': form,
        'page_title': 'Add Food Item',
    })


@login_required(login_url='custom_admin_login')
def edit_food(request, food_id):
    if not request.user.is_staff:
        return redirect('custom_admin_login')

    food = get_object_or_404(FoodItem, id=food_id)

    if request.method == 'POST':
        form = FoodItemForm(
            request.POST,
            request.FILES,
            instance=food
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'Food item updated successfully.')
            return redirect('admin_dashboard')
    else:
        form = FoodItemForm(instance=food)

    return render(request, 'menu/food_form.html', {
        'form': form,
        'food': food,
        'page_title': 'Edit Food Item',
    })


@login_required(login_url='custom_admin_login')
def delete_food(request, food_id):
    if not request.user.is_staff:
        return redirect('custom_admin_login')

    food = get_object_or_404(FoodItem, id=food_id)

    if request.method == 'POST':
        food.delete()
        messages.success(request, 'Food item deleted successfully.')

    return redirect('admin_dashboard')