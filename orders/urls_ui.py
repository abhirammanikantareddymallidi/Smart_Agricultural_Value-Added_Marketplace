from django.urls import path
from .ui_views import (
    cart_view, add_to_cart_view, update_cart_view,
    checkout_view, add_address_view, order_summary_view, place_order_view,
    order_list_view, order_detail_view
)

urlpatterns = [
    path('', order_list_view, name='ui_order_list'),
    path('<int:pk>/', order_detail_view, name='ui_order_detail'),
    path('cart/', cart_view, name='ui_cart'),
    path('cart/add/', add_to_cart_view, name='ui_add_to_cart'),
    path('cart/update/<int:item_id>/', update_cart_view, name='ui_update_cart'),
    path('checkout/', checkout_view, name='ui_checkout'),
    path('checkout/address/add/', add_address_view, name='ui_add_address'),
    path('checkout/summary/', order_summary_view, name='ui_order_summary'),
    path('checkout/place/', place_order_view, name='ui_place_order'),
]
