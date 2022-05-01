from django.contrib import messages
from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import *
from .utils import cookieCart, cartData, guestOrder 
import smtplib
# Create your views here.

def store(request):
    products = Product.objects.all()
   
    context = {
        'products': products
    }
    return render(request, 'store/store.html', context)

def cart(request):

    data = cartData(request)
    items = data['items']
    order = data['order']

    context = {
        'items': items,
        "order": order
    }

    return render(request, 'store/cart.html', context)

def checkout(request):
    
    data = cartData(request)
    items = data['items']
    order = data['order']

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
        if orderItem.quantity >= 2:
            if orderItem.product.is_available:
                messages.flash('info', 'You can only order a maximum of 2 bottles per item')
        else:
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
    if request.user.is_authenticated:
        customer = request.user.customer
        order = Order.objects.get(customer=customer, complete=False)

        if order:
            print(order.get_cart_items)
            return JsonResponse({'cart_items': order.get_cart_items})
        else:
            return JsonResponse({'cart_items': 0})
    else:
        cart_items = 0
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        
        if cart:
            for item in cart:
                cart_items += cart[item]['quantity']
            
        return JsonResponse({'cart_items': cart_items})


def process_order(request):
    data = json.loads(request.body)

    cc = ConfirmationCode.objects.create (
        code=data.get('confirmationCode'),
        name=data.get('name'),
        email=data.get('email'),
        amount=data.get('amount')
    )

    messages.add_message(request, messages.SUCCESS, 'Payment processed')
    
    #serializer = ShippingSerializer(data=request.data)
    return JsonResponse('Payment complete', safe=False)

