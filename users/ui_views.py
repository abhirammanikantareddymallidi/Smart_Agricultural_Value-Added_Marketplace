from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User

def login_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            if user.role == 'FARMER':
                return redirect('ui_my_products')
            elif user.role == 'BUYER':
                return redirect('ui_product_list')
            else:
                return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'users/login.html')

def register_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        e = request.POST.get('email')
        p = request.POST.get('password')
        r = request.POST.get('role')
        
        if User.objects.filter(username=u).exists():
            messages.error(request, "Username already exists.")
        else:
            user = User.objects.create_user(username=u, email=e, password=p, role=r)
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
            
    return render(request, 'users/register.html')

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('home')
