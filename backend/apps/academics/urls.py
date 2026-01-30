from django.urls import path
from .views import (
    AcademicsPagePublicView, AcademicsPageAdminView,
    ClassCategoryAdminView, ClassCategoryDetailAdminView,
    SubjectAdminView, SubjectDetailAdminView
)

urlpatterns = [
    # Public
    path('page/', AcademicsPagePublicView.as_view(), name='academics-page'),
    
    # Admin
    path('admin/page/', AcademicsPageAdminView.as_view(), name='admin-academics-page'),
    path('admin/categories/', ClassCategoryAdminView.as_view(), name='admin-class-categories'),
    path('admin/categories/<int:pk>/', ClassCategoryDetailAdminView.as_view(), name='admin-class-categories-detail'),
    path('admin/subjects/', SubjectAdminView.as_view(), name='admin-subjects'),
    path('admin/subjects/<int:pk>/', SubjectDetailAdminView.as_view(), name='admin-subjects-detail'),
]
