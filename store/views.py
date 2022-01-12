from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import *
from .serializers import ShippingSerializer
import datetime
# Create your views here.

def store(request):
    products = Product.objects.all()
    for product in products:
        print(product.imageURL)
    context = {
        'products': products
    }
    return render(request, 'store/store.html', context)

def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []

    context = {
        'items': items,
        "order": order
    }
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []

    context = {
        'items': items,
        "order": order
    }

    return render(request, 'store/checkout.html', context)

def update_item(request):
    data = json.loads(request.body)
    product_id = data.get('productId')
    action = data.get('action')
    
    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    print('Order created = ', created)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    print('OrderItem created = ', created)

    if action == 'add':
        orderItem.quantity += 1
        print(orderItem.quantity)
    elif action == 'remove':
        orderItem.quantity -= 1
        print(orderItem.quantity)
        
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def get_cart_total(request):
    customer = request.user.customer
    order = Order.objects.get(customer=customer, complete=False)

    if order:
        print(order.get_cart_items)
        return JsonResponse({'cart_items': order.get_cart_items})
    else:
        return JsonResponse({'cart_items': 0})

def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping:
            ShippingAddress.objects.create(
                customer = customer,
                order = order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                street = data['shipping']['street'],
                house = data['shipping']['house']
            )

    else:
        print('User not loggid in')
    #serializer = ShippingSerializer(data=request.data)
    print(data)
    return JsonResponse('Payment complete', safe=False)

