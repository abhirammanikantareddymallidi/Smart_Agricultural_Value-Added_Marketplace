from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem, Address, Cart, CartItem
from products.models import Product
from django.core.mail import send_mail
from django.conf import settings

@login_required
def cart_view(request):
    if not request.user.is_buyer():
        messages.error(request, "Only buyers have carts.")
        return redirect('ui_product_list')
    cart, created = Cart.objects.get_or_create(buyer=request.user)
    return render(request, 'orders/cart.html', {'cart': cart})

@login_required
def add_to_cart_view(request):
    if not request.user.is_buyer():
        messages.error(request, "Only buyers can add items to cart.")
        return redirect('ui_product_list')
    
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)
        
        cart, created = Cart.objects.get_or_create(buyer=request.user)
        
        # Check stock
        if product.stock_quantity < quantity:
            messages.error(request, f"Sorry, only {product.stock_quantity} available in stock.")
            return redirect('ui_product_detail', pk=product.id)
            
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            if product.stock_quantity < (cart_item.quantity + quantity):
                messages.error(request, "Cannot add more items than available in stock.")
                return redirect('ui_cart')
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
        
        messages.success(request, f"Added {product.name} to cart.")
        return redirect('ui_cart')
    return redirect('ui_product_list')

@login_required
def update_cart_view(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__buyer=request.user)
        action = request.POST.get('action')
        
        if action == 'increment':
            if cart_item.product.stock_quantity > cart_item.quantity:
                cart_item.quantity += 1
                cart_item.save()
            else:
                messages.warning(request, "Max stock reached.")
        elif action == 'decrement':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
        elif action == 'remove':
            cart_item.delete()
    return redirect('ui_cart')

@login_required
def checkout_view(request):
    cart, _ = Cart.objects.get_or_create(buyer=request.user)
    if cart.items.count() == 0:
        messages.error(request, "Your cart is empty.")
        return redirect('ui_cart')
        
    addresses = Address.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/checkout.html', {'addresses': addresses, 'cart': cart})

@login_required
def add_address_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address_line = request.POST.get('address_line')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        
        Address.objects.create(
            user=request.user, full_name=full_name, phone=phone,
            address_line=address_line, city=city, state=state, pincode=pincode
        )
        messages.success(request, "Address added successfully.")
        return redirect('ui_checkout')
    return render(request, 'orders/address_form.html')

@login_required
def order_summary_view(request):
    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        if not address_id:
            messages.error(request, "Please select a delivery address.")
            return redirect('ui_checkout')
            
        address = get_object_or_404(Address, id=address_id, user=request.user)
        cart = Cart.objects.get(buyer=request.user)
        
        # Validate stock before summary
        for item in cart.items.all():
            if item.product.stock_quantity < item.quantity:
                messages.error(request, f"Sorry, {item.product.name} is out of stock (available: {item.product.stock_quantity}). Please adjust your cart.")
                return redirect('ui_cart')

        return render(request, 'orders/order_summary.html', {'address': address, 'cart': cart})
    return redirect('ui_checkout')

@login_required
def place_order_view(request):
    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        address = get_object_or_404(Address, id=address_id, user=request.user)
        cart = Cart.objects.get(buyer=request.user)
        
        if cart.items.count() == 0:
            return redirect('ui_cart')
            
        # Final Stock Verification & Order Creation
        order = Order.objects.create(buyer=request.user, address=address, status='PENDING')
        
        for item in cart.items.all():
            product = item.product
            if product.stock_quantity < item.quantity:
                # Rollback basically
                order.delete()
                messages.error(request, f"Oops, {product.name} just went out of stock. Order cancelled.")
                return redirect('ui_cart')
                
            # Create item
            OrderItem.objects.create(
                order=order, product=product, quantity=item.quantity, price=product.price_per_half_kg
            )
            # Deduct stock
            product.stock_quantity -= item.quantity
            product.save()
            
        # Clear cart
        cart.items.all().delete()
        
        # Send email to farmers
        farmers_emails = set()
        for item in order.items.all():
            if item.product.farmer.email:
                farmers_emails.add(item.product.farmer.email)
                
        for email in farmers_emails:
            try:
                send_mail(
                    subject=f"New Order Received! (Order #{order.id})",
                    message=f"Hello,\n\nYou have received a new order for your products.\nOrder ID: {order.id}\nPlease log in to your dashboard to view the details.\n\nThank you!",
                    from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@smartagri.com'),
                    recipient_list=[email],
                    fail_silently=True,
                )
            except Exception as e:
                # Log email errors or pass
                pass
                
        messages.success(request, f"Order #{order.id} placed successfully!")
        return redirect('ui_order_detail', pk=order.pk)
    return redirect('ui_cart')

@login_required
def order_list_view(request):
    user = request.user
    if user.is_farmer():
        orders = Order.objects.filter(items__product__farmer=user).distinct().order_by('-created_at')
    elif user.is_buyer():
        orders = Order.objects.filter(buyer=user).order_by('-created_at')
    else:
        orders = Order.objects.all().order_by('-created_at')
        
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_detail_view(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.user.is_buyer() and order.buyer != request.user:
        messages.error(request, "You do not have permission to view this order.")
        return redirect('ui_order_list')
    
    return render(request, 'orders/order_detail.html', {'order': order})
