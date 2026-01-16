"""
Authentication URL patterns.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.admin_login, name='admin-login'),
    path('logout/', views.admin_logout, name='admin-logout'),
]
