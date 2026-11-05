from decimal import Decimal
from menu.models import FoodItem

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, food_id, quantity=1):
        food_id = str(food_id)
        if food_id in self.cart:
            self.cart[food_id]['quantity'] += int(quantity)
        else:
            food = FoodItem.objects.filter(id=food_id, is_available=True).first()
            if not food:
                return False
            self.cart[food_id] = {
                'quantity': int(quantity),
                'price': str(food.price),
                'name': food.name,
            }
        self.save()
        return True

    def update_quantity(self, food_id, quantity):
        food_id = str(food_id)
        qty = int(quantity)
        if qty > 0 and food_id in self.cart:
            self.cart[food_id]['quantity'] = qty
            self.save()
        elif qty <= 0 and food_id in self.cart:
            self.remove(food_id)

    def remove(self, food_id):
        food_id = str(food_id)
        if food_id in self.cart:
            del self.cart[food_id]
            self.save()

    def clear(self):
        self.session['cart'] = {}
        self.save()

    def save(self):
        self.session.modified = True

    def get_items(self):
        items = []
        total = Decimal('0.00')
        for food_id, item_data in self.cart.items():
            food = FoodItem.objects.filter(id=food_id).first()
            price = food.price if food else Decimal(item_data['price'])
            qty = item_data['quantity']
            subtotal = price * qty
            total += subtotal
            items.append({
                'food_id': food_id,
                'food': food,
                'name': food.name if food else item_data['name'],
                'price': price,
                'quantity': qty,
                'subtotal': subtotal,
                'image': food.image if food else None,
                'is_available': food.is_available if food else False,
            })
        return items, total

    def count(self):
        return sum(item['quantity'] for item in self.cart.values())
