from django.urls import path
from . import views

urlpatterns = [
    path('<int:table_number>/', views.table_qr_landing, name='table_qr_landing'),
    path('print/<int:table_number>/', views.print_table_qr, name='print_table_qr'),
] 