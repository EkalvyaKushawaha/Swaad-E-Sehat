import os

views_code = """from django.shortcuts import render, redirect, get_object_or_404
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
    total_sales = sum(o.total_amount for o in Order.objects.filter(payment_status='paid'))
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
"""

with open('orders/admin_views.py', 'w', encoding='utf-8') as f:
    f.write(views_code)

html_code = """{% extends 'base.html' %}
{% block content %}
<style>
  .dash-card { border-radius: 16px; border: none; padding: 24px; color: #fff; box-shadow: 0 10px 20px rgba(0,0,0,0.06); }
  .card-1 { background: linear-gradient(135deg, #133926, #2d6a4f); }
  .card-2 { background: linear-gradient(135deg, #e76f51, #f4a261); }
  .card-3 { background: linear-gradient(135deg, #2a9d8f, #2ec4b6); }
  .card-4 { background: linear-gradient(135deg, #457b9d, #1d3557); }
  .table-box { background: #fff; border-radius: 16px; padding: 25px; box-shadow: 0 5px 25px rgba(0,0,0,0.04); }
  .status-badge { padding: 6px 12px; border-radius: 20px; font-weight: 600; font-size: 0.8rem; }
  .btn-action { border-radius: 8px; font-size: 0.8rem; font-weight: 600; padding: 5px 12px; }
</style>

<div class='container my-5'>
  <div class='d-flex justify-content-between align-items-center mb-4'>
    <div>
      <h2 class='fw-bold' style='color:#133926;'><i class='bi bi-speedometer2 me-2'></i>Swaad-e-Sehat Executive Dashboard</h2>
      <p class='text-muted mb-0'>Live kitchen tracking, customer order confirmation aur status control.</p>
    </div>
    <div>
      <a href='/admin/' class='btn btn-outline-secondary me-2'><i class='bi bi-database me-1'></i> Master Admin</a>
      <a href='/' class='btn btn-success'><i class='bi bi-shop me-1'></i> View Cafe Site</a>
    </div>
  </div>

  <div class='row g-4 mb-4'>
    <div class='col-md-3'>
      <div class='dash-card card-1'>
        <div class='small text-white-50 text-uppercase fw-bold'>Total Orders</div>
        <h2 class='fw-bold mb-0'>{{ total_orders }}</h2>
      </div>
    </div>
    <div class='col-md-3'>
      <div class='dash-card card-2'>
        <div class='small text-white-50 text-uppercase fw-bold'>Pending Orders</div>
        <h2 class='fw-bold mb-0'>{{ pending_orders }}</h2>
      </div>
    </div>
    <div class='col-md-3'>
      <div class='dash-card card-3'>
        <div class='small text-white-50 text-uppercase fw-bold'>Completed Orders</div>
        <h2 class='fw-bold mb-0'>{{ completed_orders }}</h2>
      </div>
    </div>
    <div class='col-md-3'>
      <div class='dash-card card-4'>
        <div class='small text-white-50 text-uppercase fw-bold'>Total Sales</div>
        <h2 class='fw-bold mb-0'>Rs. {{ total_sales }}</h2>
      </div>
    </div>
  </div>

  <div class='table-box'>
    <h4 class='fw-bold mb-3' style='color:#133926;'>Customer Live Orders (Manage & Confirm)</h4>
    <div class='table-responsive'>
      <table class='table align-middle'>
        <thead class='table-light'>
          <tr>
            <th>Order No</th>
            <th>Customer</th>
            <th>Type</th>
            <th>Total Amount</th>
            <th>Current Status</th>
            <th>Change Status (Action)</th>
          </tr>
        </thead>
        <tbody>
          {% for o in recent_orders %}
          <tr>
            <td class='fw-bold text-success'>#{{ o.order_number }}</td>
            <td>
              <div class='fw-bold'>{{ o.customer_name }}</div>
              <small class='text-muted'>{{ o.phone }}</small>
            </td>
            <td><span class='badge bg-light text-dark border'>{{ o.get_order_type_display }}</span></td>
            <td class='fw-bold'>Rs. {{ o.total_amount }}</td>
            <td>
              {% if o.order_status == 'pending' %}
                <span class='badge bg-warning text-dark status-badge'>Pending Confirmation</span>
              {% elif o.order_status == 'confirmed' %}
                <span class='badge bg-info text-dark status-badge'>Confirmed</span>
              {% elif o.order_status == 'preparing' %}
                <span class='badge bg-primary status-badge'>Preparing in Kitchen</span>
              {% elif o.order_status == 'ready' %}
                <span class='badge bg-secondary status-badge'>Ready</span>
              {% elif o.order_status == 'completed' %}
                <span class='badge bg-success status-badge'>Completed</span>
              {% else %}
                <span class='badge bg-dark status-badge'>{{ o.order_status }}</span>
              {% endif %}
            </td>
            <td>
              <div class='btn-group'>
                <a href='{% url "update_order_status" o.id "confirmed" %}' class='btn btn-outline-info btn-action'>Confirm</a>
                <a href='{% url "update_order_status" o.id "preparing" %}' class='btn btn-outline-primary btn-action'>Preparing</a>
                <a href='{% url "update_order_status" o.id "completed" %}' class='btn btn-outline-success btn-action'>Complete</a>
              </div>
            </td>
          </tr>
          {% empty %}
          <tr>
            <td colspan='6' class='text-center py-4 text-muted'>Abhi koi customer order nahi hai. Aap customer page se pehla order place karke yahan dekh sakte hain!</td>
          </tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
  </div>
</div>
{% endblock %}
"""

os.makedirs('templates', exist_ok=True)
with open('templates/custom_admin_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html_code)

urls_path = 'config/urls.py'
with open(urls_path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'cafe_admin_dashboard' not in content:
    import_line = 'from orders.admin_views import admin_dashboard, update_status\n'
    route_lines = "    path('dashboard/', admin_dashboard, name='cafe_admin_dashboard'),\n    path('dashboard/status/<int:order_id>/<str:new_status>/', update_status, name='update_order_status'),\n"
    content = import_line + content
    target = 'urlpatterns = ['
    idx = content.find(target)
    if idx != -1:
        content = content[:idx+len(target)] + '\n' + route_lines + content[idx+len(target):]
        with open(urls_path, 'w', encoding='utf-8') as f:
            f.write(content)

print('\n>>> SUCCESS: Executive Dashboard Ready! <<<\n')