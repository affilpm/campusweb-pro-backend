"""
Custom permissions for Admin Authentication.
"""

from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admin users.
    Checks if the user is authenticated, active, and has staff status.
    """
    message = 'You must be an admin user to access this resource.'
    
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_active and
            request.user.is_staff
        )


class IsSuperAdmin(permissions.BasePermission):
    """
    Custom permission to only allow super admin users.
    """
    message = 'You must be a super admin to access this resource.'
    
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_active and
            request.user.is_superuser
        )


class IsOwnerOrSuperAdmin(permissions.BasePermission):
    """
    Custom permission to allow owners or super admins.
    Object-level permission.
    """
    message = 'You can only access your own data unless you are a super admin.'
    
    def has_object_permission(self, request, view, obj):
        # Super admins can access everything
        if request.user.is_superuser:
            return True
        
        # Users can only access their own objects
        return obj == request.user or getattr(obj, 'user', None) == request.user
