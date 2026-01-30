from django.urls import path
from .views import (
    GalleryPublicView, GalleryCategoryDetailView, GalleryAdminView,
    GalleryCategoryAdminView, GalleryCategoryDetailAdminView,
    GalleryImageAdminView, GalleryImageDetailAdminView
)

urlpatterns = [
    # Public
    path('', GalleryPublicView.as_view(), name='gallery-list'),
    path('category/<slug:slug>/', GalleryCategoryDetailView.as_view(), name='gallery-category'),
    
    # Admin
    path('admin/', GalleryAdminView.as_view(), name='admin-gallery'),
    path('admin/categories/', GalleryCategoryAdminView.as_view(), name='admin-categories'),
    path('admin/categories/<int:pk>/', GalleryCategoryDetailAdminView.as_view(), name='admin-categories-detail'),
    path('admin/images/', GalleryImageAdminView.as_view(), name='admin-images'),
    path('admin/images/<int:pk>/', GalleryImageDetailAdminView.as_view(), name='admin-images-detail'),
]
