from django.urls import path
from . import views

urlpatterns = [
    path('', views.delivery_dashboard, name='delivery_dashboard'),
    path('update/<int:assignment_id>/', views.update_delivery_status, name='update_delivery_status'),
]
