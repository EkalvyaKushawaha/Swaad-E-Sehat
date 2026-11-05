# from django.shortcuts import render

# Create your views here.
from decimal import Decimal

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from menu.models import FoodItem
from .models import Order, OrderItem


def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = Decimal('0.00')

    for food_id, quantity in cart.items():
        food = FoodItem.objects.filter(
            id=food_id,
            is_available=True
        ).first()

        if food is None:
            continue

        quantity = int(quantity)
        subtotal = food.price * quantity

        cart_items.append({
            'food': food,
            'quantity': quantity,
            'subtotal': subtotal,
        })

        total += subtotal

    return render(request, 'orders/cart.html', {
        'cart_items': cart_items,
        'total': total,
    })


@require_POST
def add_to_cart(request, food_id):
    food = get_object_or_404(
        FoodItem,
        id=food_id,
        is_available=True
    )

    cart = request.session.get('cart', {})
    key = str(food.id)

    quantity = int(cart.get(key, 0))

    if quantity < 99:
        cart[key] = quantity + 1

    request.session['cart'] = cart
    request.session.modified = True

    messages.success(
        request,
        f'{food.name} cart mein add ho gaya!'
    )

    return redirect('cart_detail')


@require_POST
def update_cart(request, food_id):
    cart = request.session.get('cart', {})
    key = str(food_id)

    if key in cart:
        try:
            quantity = int(request.POST.get('quantity', 1))
        except (TypeError, ValueError):
            quantity = 1

        if quantity <= 0:
            cart.pop(key, None)
        else:
            cart[key] = min(quantity, 99)

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart_detail')


@require_POST
def remove_from_cart(request, food_id):
    cart = request.session.get('cart', {})
    cart.pop(str(food_id), None)

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart_detail')


def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        messages.error(request, 'Tumhara cart khaali hai.')
        return redirect('cart_detail')

    cart_items = []
    total = Decimal('0.00')

    for food_id, quantity in cart.items():
        food = FoodItem.objects.filter(
            id=food_id,
            is_available=True
        ).first()

        if food is None:
            continue

        quantity = int(quantity)
        subtotal = food.price * quantity

        cart_items.append({
            'food': food,
            'quantity': quantity,
            'subtotal': subtotal,
        })

        total += subtotal

    if not cart_items:
        messages.error(request, 'Cart mein koi available food item nahi hai.')
        return redirect('cart_detail')

    if request.method == 'POST':
        customer_name = request.POST.get('customer_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        order_type = request.POST.get('order_type', '').strip()
        address = request.POST.get('address', '').strip()
        table_number_text = request.POST.get('table_number', '').strip()

        valid_types = {'dine_in', 'takeaway', 'delivery'}

        if not customer_name or not phone:
            messages.error(request, 'Naam aur phone number zaroori hain.')
        elif order_type not in valid_types:
            messages.error(request, 'Sahi order type select karo.')
        elif order_type == 'delivery' and not address:
            messages.error(request, 'Home delivery ke liye address zaroori hai.')
        else:
            table_number = None

            if order_type == 'dine_in':
                try:
                    table_number = int(table_number_text)
                    if table_number <= 0:
                        raise ValueError
                except (TypeError, ValueError):
                    messages.error(
                        request,
                        'Dine-in ke liye valid table number daalo.'
                    )
                    return render(request, 'orders/checkout.html', {
                        'cart_items': cart_items,
                        'total': total,
                    })

            order = Order.objects.create(
                customer_name=customer_name,
                phone=phone,
                order_type=order_type,
                address=address if order_type == 'delivery' else '',
                table_number=table_number,
                total_amount=total,
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    food=item['food'],
                    quantity=item['quantity'],
                    price=item['food'].price,
                )

            request.session['cart'] = {}
            request.session.modified = True

            return render(request, 'orders/order_success.html', {
                'order': order,
            })

    return render(request, 'orders/checkout.html', {
        'cart_items': cart_items,
        'total': total,
    })