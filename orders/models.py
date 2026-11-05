import uuid, time, random
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from menu.models import FoodItem
from tables.models import CafeTable

class Order(models.Model):
    TYPES = (('dine_in', 'Dine-in'), ('takeaway', 'Takeaway'), ('delivery', 'Home Delivery'))
    STATUSES = (
        ('pending', 'Pending'), ('confirmed', 'Confirmed'), ('preparing', 'Preparing'),
        ('ready', 'Ready'), ('out_for_delivery', 'Out for Delivery'),
        ('completed', 'Completed'), ('cancelled', 'Cancelled')
    )
    order_number = models.CharField(max_length=30, unique=True, editable=False)
    access_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    customer_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    order_type = models.CharField(max_length=20, choices=TYPES, default='takeaway')
    table = models.ForeignKey(CafeTable, on_delete=models.SET_NULL, null=True, blank=True)
    delivery_address = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    order_status = models.CharField(max_length=25, choices=STATUSES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"SES-{time.strftime('%y%m%d')}-{random.randint(1000, 9999)}"
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    food_item = models.ForeignKey(FoodItem, on_delete=models.SET_NULL, null=True, blank=True)
    food_name = models.CharField(max_length=150)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
