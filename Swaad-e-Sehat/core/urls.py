from django.urls import path
from . import views

urlpatterns = [
path('', views.home, name='home'),
path('cafe-admin/login/', views.admin_login, name='custom_admin_login'),
path('cafe-admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
path('cafe-admin/logout/', views.admin_logout, name='admin_logout'),
]