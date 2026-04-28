from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product
from .models import Product

def product_list_view(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'products/product_list.html', {'products': products})

def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})

@login_required
def my_products_view(request):
    if not request.user.is_farmer():
        messages.error(request, "Only farmers can view this page.")
        return redirect('ui_product_list')
    products = Product.objects.filter(farmer=request.user).order_by('-created_at')
    return render(request, 'products/my_products.html', {'products': products})

@login_required
def add_product_view(request):
    if not request.user.is_farmer():
        messages.error(request, "Only farmers can add products.")
        return redirect('ui_product_list')
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price_per_half_kg')
        stock = request.POST.get('stock_quantity')
        category = request.POST.get('category')
        image = request.FILES.get('product_image')
        
        Product.objects.create(
            farmer=request.user,
            name=name,
            description=description,
            price_per_half_kg=price,
            stock_quantity=stock,
            category=category,
            product_image=image
        )
        messages.success(request, "Product added successfully!")
        return redirect('ui_my_products')
    return render(request, 'products/add_product.html')
