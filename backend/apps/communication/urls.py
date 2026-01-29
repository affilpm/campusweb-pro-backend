from django.urls import path
from .views import (
    NoticesPublicView, NoticeDetailPublicView,
    EventsPublicView, EventDetailPublicView,
    NoticeAdminView, NoticeDetailAdminView,
    EventAdminView, EventDetailAdminView
)

urlpatterns = [
    # Public
    path('notices/', NoticesPublicView.as_view(), name='notices-list'),
    path('notices/<slug:slug>/', NoticeDetailPublicView.as_view(), name='notice-detail'),
    path('events/', EventsPublicView.as_view(), name='events-list'),
    path('events/<slug:slug>/', EventDetailPublicView.as_view(), name='event-detail'),
    
    # Admin
    path('admin/notices/', NoticeAdminView.as_view(), name='admin-notices'),
    path('admin/notices/<int:pk>/', NoticeDetailAdminView.as_view(), name='admin-notices-detail'),
    path('admin/events/', EventAdminView.as_view(), name='admin-events'),
    path('admin/events/<int:pk>/', EventDetailAdminView.as_view(), name='admin-events-detail'),
]
