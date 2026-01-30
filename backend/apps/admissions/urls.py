from django.urls import path
from .views import (
    AdmissionsPagePublicView, AdmissionStatusPublicView, 
    AdmissionSettingsAdminView, AdmissionStepAdminView, 
    AdmissionStepDetailAdminView
)

urlpatterns = [
    # Public
    path('public/init/', AdmissionsPagePublicView.as_view(), name='admissions-page'),
    path('status/', AdmissionStatusPublicView.as_view(), name='admissions-status'),
    
    # Admin
    path('admin/settings/', AdmissionSettingsAdminView.as_view(), name='admin-admissions-settings'),
    path('admin/steps/', AdmissionStepAdminView.as_view(), name='admin-admissions-steps'),
    path('admin/steps/<int:pk>/', AdmissionStepDetailAdminView.as_view(), name='admin-admissions-steps-detail'),
]
