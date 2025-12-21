from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    # API Routes
    path('api/admin/auth/', include('authentication.urls')),
    
    # Content API (reverting to monolithic structure)
    path('api/', include('content.urls')),
]

# Static/Media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
