import socket
from django.shortcuts import render, get_object_or_404, redirect
from .models import CafeTable

def table_qr_landing(request, table_number):
    table = get_object_or_404(CafeTable, table_number=table_number, is_active=True)
    request.session['dine_in_table_number'] = table.table_number
    request.session['dine_in_table_id'] = table.id
    return redirect('menu_list')

def print_table_qr(request, table_number):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except Exception:
        local_ip = "127.0.0.1"

    port = request.get_port()
    qr_url = f"http://{local_ip}:{port}/tables/{table_number}/"

    return render(request, 'tables/print_qr.html', {
        'table_number': table_number,
        'qr_url': qr_url
    })