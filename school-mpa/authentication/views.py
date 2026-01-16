"""
Authentication views - session-based login/logout.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect


@csrf_protect
@require_http_methods(["GET", "POST"])
def admin_login(request):
    """Admin login view with session-based authentication."""
    if request.user.is_authenticated:
        return redirect('admin-dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        
        if not email or not password:
            messages.error(request, 'Please enter both email and password.')
            return render(request, 'admin/login.html')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                next_url = request.GET.get('next', 'admin-dashboard')
                messages.success(request, f'Welcome back, {user.get_short_name()}!')
                return redirect(next_url)
            else:
                messages.error(request, 'Your account has been deactivated.')
        else:
            messages.error(request, 'Invalid email or password.')
    
    return render(request, 'admin/login.html')


@require_http_methods(["GET", "POST"])
def admin_logout(request):
    """Admin logout view."""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')
