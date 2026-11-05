from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from orders.models import Order
from menu.models import FoodItem
from tables.models import CafeTable
from delivery.models import DeliveryAssignment

@staff_member_required
def admin_dashboard(request):
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(order_status='pending').count()
    completed_orders = Order.objects.filter(order_status='completed').count()
    total_sales = sum(o.total_amount for o in Order.objects.filter(order_status='completed'))
    recent_orders = Order.objects.all().order_by('-created_at')[:15]
    tables = CafeTable.objects.all()
    
    context = {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
        'total_sales': total_sales,
        'recent_orders': recent_orders,
        'tables': tables,
    }
    return render(request, 'custom_admin_dashboard.html', context)

@staff_member_required
def update_status(request, order_id, new_status):
    order = get_object_or_404(Order, id=order_id)
    order.order_status = new_status
    order.save()
    return redirect('cafe_admin_dashboard')
