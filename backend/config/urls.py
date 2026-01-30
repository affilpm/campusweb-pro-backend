from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Public MPA Routes
    path('', include('apps.landing.urls')),
    
    # API Routes
    # API Routes (v1)
    path('api/v1/auth/', include('apps.authentication.urls')),
    path('api/v1/landing/', include('apps.landing.urls')),
    path('api/v1/school-info/', include('apps.school_info.urls')),
    path('api/v1/communication/', include('apps.communication.urls')),
    path('api/v1/gallery/', include('apps.gallery.urls')),
    path('api/v1/academics/', include('apps.academics.urls')),
    path('api/v1/admissions/', include('apps.admissions.urls')),
]


# Static/Media
if settings.DEBUG:
    if settings.MEDIA_URL and not settings.MEDIA_URL.startswith(('http://', 'https://')):
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    if settings.STATIC_URL and not settings.STATIC_URL.startswith(('http://', 'https://')):
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
