from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from menu.models import FoodItem
from orders.models import Order

def home(request):
    food_items = FoodItem.objects.filter(is_available=True)
    return render(request, 'core/home.html', {
        'food_items': food_items
    })

def admin_login(request):
    error = ''

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            error = 'Invalid username or password.'

    return render(
        request,
        'core/admin_login.html',
        {'error': error}
    )

@login_required(login_url='custom_admin_login')
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('custom_admin_login')

# Update order status
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')

        valid_statuses = [
            'pending',
            'confirmed',
            'preparing',
            'ready',
            'completed',
            'cancelled',
        ]

        if new_status in valid_statuses and order_id:
            Order.objects.filter(id=order_id).update(
                status=new_status
            )

        return redirect('admin_dashboard')

    context = {
        'total_orders': Order.objects.count(),
        'pending_orders': Order.objects.filter(
            status='pending'
        ).count(),
        'preparing_orders': Order.objects.filter(
        status='preparing'
        ).count(),
        'completed_orders': Order.objects.filter(
            status='completed'
        ).count(),
        'orders': Order.objects.all().order_by(
            '-created_at'
        )[:20],
        'food_items': FoodItem.objects.all(),
        'status_choices': Order.ORDER_STATUS,
    }

    return render(
        request,
        'core/admin_dashboard.html',
        context
    )

def admin_logout(request):
    logout(request)
    return redirect('custom_admin_login') 