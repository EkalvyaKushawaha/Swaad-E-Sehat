from django.db import models
from django.contrib.auth.models import User

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True, null=True)
    is_delivery_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Address(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    house_flat = models.CharField(max_length=100)
    street = models.CharField(max_length=150)
    area = models.CharField(max_length=150)
    city = models.CharField(max_length=100, default='Lucknow')
    state = models.CharField(max_length=100, default='Uttar Pradesh')
    pin_code = models.CharField(max_length=10)
    landmark = models.CharField(max_length=150, blank=True, null=True)
