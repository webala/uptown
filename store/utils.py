import json
from .models import *

def cookieCart(request):
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}

        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}

        if cart:
            for item in cart:
                product = Product.objects.get(id=item)
                total = product.price * cart[item]['quantity']

                order['get_cart_total'] += total
                order['get_cart_items'] += cart[item]['quantity']

                order_item = {
                    'product': {
                        'id': product.id,
                        'name': product.name,
                        'price': product.price,
                        'imageURL': product.imageURL    
                    },
                    'quantity': cart[item]['quantity'],
                    'get_total': total
                }

                items.append(order_item)

                if not product.digital:
                    order['shipping'] = True
    
        return {'order': order, 'items': items}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer, complete=False)
        items = order.orderitem_set.all()
    else:
        cookieData = cookieCart(request)
        items = cookieData['items']
        order = cookieData['order']    
    return {'order': order, 'items': items}