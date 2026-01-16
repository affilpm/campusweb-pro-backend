"""
Public site URL patterns.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Homepage
    path('', views.home, name='home'),
    
    # About
    path('about/', views.about, name='about'),
    
    # Academics
    path('academics/', views.academics, name='academics'),
    
    # Admissions
    path('admissions/', views.admissions, name='admissions'),
    
    # Contact
    path('contact/', views.contact, name='contact'),
    
    # Facilities
    path('facilities/', views.facilities, name='facilities'),
    path('facilities/<slug:slug>/', views.facility_detail, name='facility-detail'),
    
    # Gallery
    path('gallery/', views.gallery, name='gallery'),
    
    # Notices
    path('notices/', views.notices, name='notices'),
    path('notices/<int:pk>/', views.notice_detail, name='notice-detail'),
    
    # Events
    path('events/', views.events, name='events'),
    path('events/<slug:slug>/', views.event_detail, name='event-detail'),
    
    # Public Disclosure
    path('public-disclosure/', views.public_disclosure, name='public-disclosure'),
]
