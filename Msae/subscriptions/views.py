from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from .models import SaladSubscription

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('welcome')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def index_view(request):
    

    return render(request, 'index.html')

@login_required
def welcome_view(request):
    subscription = SaladSubscription.objects.filter(user=request.user, is_active=True).first()
    
    if request.method == 'POST':
        plan = request.POST.get('plan')
        address = request.POST.get('address')
        
        # Create or update subscription
        SaladSubscription.objects.update_or_create(
            user=request.user,
            is_active=True,
            defaults={'plan': plan, 'delivery_address': address, 'order_status': 'pending'}
        )
        return redirect('welcome')

    return render(request, 'welcome.html', {'subscription': subscription})

def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
def admin_dashboard_view(request):
    if request.method == 'POST':
        sub_id = request.POST.get('subscription_id')
        new_status = request.POST.get('order_status')
        subscription = get_object_or_404(SaladSubscription, id=sub_id)
        subscription.order_status = new_status
        subscription.save()
        return redirect('admin_dashboard')

    subscriptions = SaladSubscription.objects.all().order_by('-start_date')
    return render(request, 'admin_dashboard.html', {'subscriptions': subscriptions})