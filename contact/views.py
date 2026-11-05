from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage

def contact_view(request):
    if request.method == 'POST':
        ContactMessage.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message')
        )
        messages.success(request, 'Aapka message receive ho gaya hai! Hamari team aapse jaldi contact karegi.')
        return redirect('contact')
    return render(request, 'contact/contact.html')
