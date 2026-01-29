from django.urls import path
from .views import (
    LandingHomeView, HeroAdminView, HomeAboutAdminView,
    AcademicHighlightAdminView, AcademicHighlightDetailAdminView
)

urlpatterns = [
    path('home/', LandingHomeView.as_view(), name='home'),
    
    # Admin
    path('admin/hero/', HeroAdminView.as_view(), name='admin-hero'),
    path('admin/home-about/', HomeAboutAdminView.as_view(), name='admin-home-about'),
    path('admin/highlights/', AcademicHighlightAdminView.as_view(), name='admin-highlights'),
    path('admin/highlights/<int:pk>/', AcademicHighlightDetailAdminView.as_view(), name='admin-highlights-detail'),
]
