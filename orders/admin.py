from django.contrib import admin
from .models import Order, OrderItem, Review, Address, Cart, CartItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('buyer__username',)
    inlines = [OrderItemInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'buyer', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'city', 'state', 'pincode')

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'created_at')
    inlines = [CartItemInline]
