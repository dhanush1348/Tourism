from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import User, Wishlist
from bookings.models import Tour
from .forms import CustomSignupForm, CustomLoginForm
from django.views.generic import View

# Create your views here.

@login_required
def profile(request):
    """Display user profile."""
    user = request.user
    wishlist = Wishlist.objects.filter(user=user).select_related('tour')
    return render(request, 'accounts/profile.html', {
        'user': user,
        'wishlist': wishlist
    })

@login_required
def profile_edit(request):
    """Edit user profile."""
    if request.method == 'POST':
        # Handle profile update logic here
        messages.success(request, 'Profile updated successfully!')
        return redirect('accounts:profile')
    return render(request, 'accounts/profile_edit.html')

@login_required
def change_password(request):
    """Change user password."""
    if request.method == 'POST':
        # Handle password change logic here
        messages.success(request, 'Password changed successfully!')
        return redirect('accounts:profile')
    return render(request, 'accounts/change_password.html')

@login_required
def notifications(request):
    return render(request, 'accounts/notifications.html')

@login_required
def preferences(request):
    if request.method == 'POST':
        user = request.user
        user.preferred_currency = request.POST.get('preferred_currency', user.preferred_currency)
        user.preferred_language = request.POST.get('preferred_language', user.preferred_language)
        user.travel_style = request.POST.get('travel_style', user.travel_style)
        user.email_notifications = 'email_notifications' in request.POST
        user.sms_notifications = 'sms_notifications' in request.POST
        user.save()
        
        messages.success(request, 'Your preferences have been updated successfully.')
        return redirect('accounts:profile')
    
    return render(request, 'accounts/preferences.html')

@login_required
@require_POST
def toggle_wishlist(request, tour_id):
    """Add or remove a tour from the user's wishlist."""
    tour = get_object_or_404(Tour, id=tour_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, tour=tour)
    
    if not created:
        wishlist_item.delete()
        return JsonResponse({'status': 'removed', 'message': 'Tour removed from wishlist'})
    
    return JsonResponse({'status': 'added', 'message': 'Tour added to wishlist'})

@login_required
def wishlist_view(request):
    """Display user's wishlist."""
    wishlist = Wishlist.objects.filter(user=request.user).select_related('tour')
    return render(request, 'accounts/wishlist.html', {
        'wishlist': wishlist
    })

class SignupView(View):
    def get(self, request):
        form = CustomSignupForm()
        return render(request, 'account/signup.html', {'form': form})

    def post(self, request):
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('accounts:login')
        return render(request, 'account/signup.html', {'form': form})

def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('core:home')

def login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('core:home')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = CustomLoginForm()
    
    return render(request, 'account/login.html', {'form': form})

# Update the URL patterns to use these class-based views
signup = SignupView.as_view()
login = login
