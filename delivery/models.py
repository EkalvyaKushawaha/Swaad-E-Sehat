import urllib.parse
from django.db import models
from django.contrib.auth.models import User
from orders.models import Order

class DeliveryAssignment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='delivery_assignment')
    delivery_staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_deliveries')
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_at = models.DateTimeField(auto_now_add=True)
    delivery_status = models.CharField(max_length=25, default='assigned')

    def google_maps_directions_url(self):
        if self.order.delivery_address:
            return f"https://www.google.com/maps/dir/?api=1&destination={urllib.parse.quote(self.order.delivery_address)}"
        return "https://www.google.com/maps"
