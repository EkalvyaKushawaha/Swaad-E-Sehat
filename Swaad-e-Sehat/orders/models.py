from django.db import models


class Order(models.Model):
    ORDER_TYPES = [
        ('dine_in', 'Dine In'),
        ('takeaway', 'Takeaway'),
        ('delivery', 'Home Delivery'),
    ]

    ORDER_STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    order_type = models.CharField(
        max_length=20,
        choices=ORDER_TYPES
    )
    address = models.TextField(blank=True)
    table_number = models.PositiveIntegerField(
        null=True,
        blank=True
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    food = models.ForeignKey(
        'menu.FoodItem',
        on_delete=models.PROTECT
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.food.name} x {self.quantity}"

    @property
    def subtotal(self):
        return self.price * self.quantity