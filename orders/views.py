from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib import messages
from .cart import Cart
from .models import Order, OrderItem
from tables.models import CafeTable

def cart_view(request):
    cart = Cart(request)
    items, total = cart.get_items()
    return render(request, 'orders/cart.html', {'items': items, 'total': total})

def add_to_cart(request, food_id):
    qty = request.POST.get('quantity', 1)
    Cart(request).add(food_id, qty)
    return redirect(request.META.get('HTTP_REFERER', 'cart'))

def update_cart(request, food_id):
    qty = request.POST.get('quantity', 1)
    Cart(request).update_quantity(food_id, qty)
    return redirect('cart')

def remove_from_cart(request, food_id):
    Cart(request).remove(food_id)
    return redirect('cart')

def checkout(request):
    cart = Cart(request)
    items, total = cart.get_items()
    if not items:
        return redirect('menu_list')

    table_num = request.session.get('dine_in_table_number')
    table_id = request.session.get('dine_in_table_id')

    if request.method == 'POST':
        order_type = request.POST.get('order_type')
        if not order_type:
            order_type = 'dine_in' if table_id else 'takeaway'

        name = request.POST.get('customer_name', '').strip()
        if not name:
            name = f"Guest @ Table {table_num}" if table_num else "Walk-in Guest"

        phone = request.POST.get('phone', '').strip() or 'N/A'
        notes = request.POST.get('notes', '')

        table_obj = None
        delivery_addr = ''

        if order_type == 'dine_in':
            tid = request.POST.get('table_id') or table_id
            if tid:
                table_obj = CafeTable.objects.filter(id=tid).first()
        elif order_type == 'delivery':
            delivery_addr = f"{request.POST.get('house_flat')}, {request.POST.get('street')}, {request.POST.get('area')}, {request.POST.get('city', 'Lucknow')} - {request.POST.get('pin_code')}"

        with transaction.atomic():
            order = Order.objects.create(
                customer=request.user if request.user.is_authenticated else None,
                customer_name=name,
                phone=phone,
                order_type=order_type,
                table=table_obj,
                delivery_address=delivery_addr,
                notes=notes,
                total_amount=Decimal('0.00'),
            )
            calc_total = Decimal('0.00')
            for itm in items:
                food = itm['food']
                price = food.price if food else itm['price']
                subtot = price * itm['quantity']
                calc_total += subtot
                OrderItem.objects.create(
                    order=order,
                    food_item=food,
                    food_name=itm['name'],
                    unit_price=price,
                    quantity=itm['quantity'],
                    subtotal=subtot
                )
            order.total_amount = calc_total
            order.save()

        cart.clear()
        return redirect('order_confirmation', access_token=order.access_token)

    return render(request, 'orders/checkout.html', {
        'items': items,
        'total': total,
        'table_num': table_num,
        'table_id': table_id
    })

def order_confirmation(request, access_token):
    order = get_object_or_404(Order, access_token=access_token)
    return render(request, 'orders/order_confirmation.html', {'order': order})

def order_tracking(request, access_token):
    order = get_object_or_404(Order, access_token=access_token)
    return render(request, 'orders/order_tracking.html', {'order': order})

def my_orders(request):
    if not request.user.is_authenticated:
        return redirect('login')
    orders = Order.objects.filter(customer=request.user)
    return render(request, 'orders/my_orders.html', {'orders': orders})