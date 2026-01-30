"""
URL patterns for Admin Authentication.
"""

from django.urls import path
from .views import (
    AdminLoginView,
    AdminLogoutView,
    TokenRefreshView,
    AdminMeView,
    AdminVerifyTokenView,
)

app_name = 'authentication'

urlpatterns = [
    path('login/', AdminLoginView.as_view(), name='login'),
    path('logout/', AdminLogoutView.as_view(), name='logout'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', AdminMeView.as_view(), name='me'),
    path('verify/', AdminVerifyTokenView.as_view(), name='verify'),
]
