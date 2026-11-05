from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:food_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:food_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('confirm/<uuid:access_token>/', views.order_confirmation, name='order_confirmation'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('track/<uuid:access_token>/', views.order_tracking, name='order_tracking'),
]
