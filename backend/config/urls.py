"""
URL configuration for School Backend.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import URLs from all apps
# Legacy Content app fallbacks
from content.views import HomepagePublicView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API Routes
    path('api/admin/auth/', include('authentication.urls')),
    
    # Content API (reverting to monolithic structure)
    path('api/', include('content.urls')),
]

# Static/Media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
