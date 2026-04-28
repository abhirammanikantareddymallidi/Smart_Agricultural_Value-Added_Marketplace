from rest_framework import serializers
from .models import Order, OrderItem, Review, Address, Cart, CartItem
from products.models import Product

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ('user',)

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    price_per_half_kg = serializers.DecimalField(source='product.price_per_half_kg', max_digits=10, decimal_places=2, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'product_name', 'quantity', 'price_per_half_kg', 'total_price')

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ('id', 'buyer', 'items', 'total_price', 'created_at')

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'product_name', 'quantity', 'price')

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'buyer', 'address', 'status', 'total_price', 'items', 'created_at', 'updated_at')
        read_only_fields = ('buyer', 'status', 'total_price')

class ReviewSerializer(serializers.ModelSerializer):
    buyer_name = serializers.CharField(source='buyer.username', read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'product', 'buyer', 'buyer_name', 'rating', 'comment', 'created_at')
        read_only_fields = ('buyer',)
