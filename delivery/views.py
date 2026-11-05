from django.shortcuts import render, redirect, get_object_or_404
from .models import DeliveryAssignment

def delivery_dashboard(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'profile') or not request.user.profile.is_delivery_staff:
        return redirect('login')
    assignments = DeliveryAssignment.objects.filter(delivery_staff=request.user).order_by('-assigned_at')
    return render(request, 'delivery/dashboard.html', {'assignments': assignments})

def update_delivery_status(request, assignment_id):
    assignment = get_object_or_404(DeliveryAssignment, id=assignment_id)
    new_status = request.POST.get('status')
    if new_status:
        assignment.delivery_status = new_status
        assignment.save()
        if new_status == 'delivered':
            assignment.order.order_status = 'completed'
            assignment.order.save()
    return redirect('delivery_dashboard')
