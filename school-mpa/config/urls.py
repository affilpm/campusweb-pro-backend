"""
URL configuration for School Website MPA.
"""

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Public pages
    path('', include('public_site.urls')),
    
    # Admin panel
    path('admin/', include('admin_panel.urls')),
    
    # Authentication
    path('auth/', include('authentication.urls')),
]

# Static/Media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
