from django.urls import path, include
from .views import *

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'confirmation_code', ConfirmationoCodeViewset, 'confirmation_code')

urlpatterns =  [
    path('', store, name='store'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('update_item/', update_item, name='update_item'),
    path('get_cart_total/', get_cart_total, name='get_cart_total'),
    path('process_order/', process_order, name='process_order'),
    path('all_products/', all_products, name='all_products'),
    path('cart_items', cart_items, name='cart_items'),
    path('api/', include(router.urls))
]