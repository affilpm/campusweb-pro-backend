"""
Admin panel URL patterns.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='admin-dashboard'),
    
    # Site Settings
    path('settings/', views.site_settings, name='admin-settings'),
    
    # Notices
    path('notices/', views.notices_list, name='admin-notices'),
    path('notices/create/', views.notice_create, name='admin-notice-create'),
    path('notices/<int:pk>/edit/', views.notice_edit, name='admin-notice-edit'),
    path('notices/<int:pk>/delete/', views.notice_delete, name='admin-notice-delete'),
    
    # Events
    path('events/', views.events_list, name='admin-events'),
    path('events/create/', views.event_create, name='admin-event-create'),
    path('events/<int:pk>/edit/', views.event_edit, name='admin-event-edit'),
    path('events/<int:pk>/delete/', views.event_delete, name='admin-event-delete'),
    
    # Contact Submissions
    path('contact/', views.contact_submissions_list, name='admin-contact-submissions'),
    path('contact/<int:pk>/', views.contact_submission_detail, name='admin-contact-detail'),
    path('contact/<int:pk>/delete/', views.contact_submission_delete, name='admin-contact-delete'),
]
