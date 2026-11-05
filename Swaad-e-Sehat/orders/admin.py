from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('food', 'quantity', 'price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer_name',
        'phone',
        'order_type',
        'total_amount',
        'status',
        'created_at',
    )

    list_filter = ('order_type', 'status', 'created_at')
    search_fields = ('customer_name', 'phone')
    list_editable = ('status',)
    inlines = [OrderItemInline]