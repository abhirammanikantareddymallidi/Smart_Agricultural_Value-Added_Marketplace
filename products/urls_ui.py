from django.urls import path
from .ui_views import product_list_view, product_detail_view, my_products_view, add_product_view

urlpatterns = [
    path('', product_list_view, name='ui_product_list'),
    path('my-products/', my_products_view, name='ui_my_products'),
    path('add/', add_product_view, name='ui_add_product'),
    path('<int:pk>/', product_detail_view, name='ui_product_detail'),
]
