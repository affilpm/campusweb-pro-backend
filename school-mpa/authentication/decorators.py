"""
Decorators for admin access control.
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def admin_required(view_func):
    """
    Decorator to require admin authentication.
    Redirects to login page if not authenticated.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please log in to access this page.')
            return redirect('admin-login')
        return view_func(request, *args, **kwargs)
    return wrapper


def role_required(*roles):
    """
    Decorator to require specific admin roles.
    Usage: @role_required('super_admin', 'admin')
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.warning(request, 'Please log in to access this page.')
                return redirect('admin-login')
            
            if request.user.role not in roles:
                messages.error(request, 'You do not have permission to access this page.')
                return redirect('admin-dashboard')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def super_admin_required(view_func):
    """Decorator to require super admin role."""
    return role_required('super_admin')(view_func)
