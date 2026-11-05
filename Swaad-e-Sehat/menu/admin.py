from django.contrib import admin

# Register your models here.
from .models import FoodItem

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
     list_display = ('name', 'price', 'is_available')
list_filter = ('is_available',)
search_fields = ('name', 'description')
list_editable = ('price', 'is_available')