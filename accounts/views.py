from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import CustomerProfile

def user_register(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        e = request.POST.get('email')
        p = request.POST.get('password')
        ph = request.POST.get('phone')
        if User.objects.filter(username=u).exists():
            messages.error(request, 'Username already taken.')
            return redirect('register')
        user = User.objects.create_user(username=u, email=e, password=p)
        CustomerProfile.objects.create(user=user, phone=ph)
        messages.success(request, 'Registration successful. Please login.')
        return redirect('login')
    return render(request, 'accounts/register.html')

def user_login(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(username=u, password=p)
        if user:
            login(request, user)
            return redirect('home')
        messages.error(request, 'Invalid credentials.')
    return render(request, 'accounts/login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

def profile(request):
    return render(request, 'accounts/profile.html')
