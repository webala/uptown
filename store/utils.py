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
                if product.discount_price:
                    total = product.discount_price * cart[item]['quantity']
                else:
                    total = product.actual_price * cart[item]['quantity']

                order['get_cart_total'] += total
                order['get_cart_items'] += cart[item]['quantity']

                order_item = {
                    'product': {
                        'id': product.id,
                        'name': product.name,
                        'price': product.discount_price if product.discount_price else product.actual_price,
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


def guestOrder(request, data):
    print('User not loggid in')

    print('COOKIES: ', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer = customer,
        complete=False
    )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        order_item = OrderItem.objects.create(
            product = product,
            order = order,
            quantity = item['quantity']
        )
    return customer, order