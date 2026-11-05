from orders.cart import Cart

def cart_processor(request):
    return {'cart_total_count': Cart(request).count()}
