from django.urls import path
from .views import (
    LayoutPublicView, AboutPagePublicView, ContactPagePublicView, PublicDisclosureView, 
    FacilitiesPublicView, FacilityDetailPublicView,
    SiteSettingsAdminView, VisionMissionAdminView, PrincipalMessageAdminView, PrincipalMessageResetView, PageSEOPublicView,
    QuickLinkAdminView, QuickLinkDetailAdminView,
    FacilityAdminView, FacilityDetailAdminView,
    FacilityGalleryAdminView, FacilityImageDetailAdminView,
    TestimonialAdminView, TestimonialDetailAdminView,
    PageSEOAdminView, PageSEODetailAdminView,
    AchievementAdminView, AchievementDetailAdminView,
    GeneralInfoAdminView, GeneralInfoDetailAdminView,
    InfrastructureAdminView, InfrastructureDetailAdminView,
    ResultsAdminView, ResultsDetailAdminView,
    FeesAdminView, FeesDetailAdminView,
    DocumentationAdminView, DocumentationDetailAdminView,
    AboutPageAdminView, TimelineEventAdminView, TimelineEventDetailAdminView,
    ManagementMemberAdminView, ManagementMemberDetailAdminView,
    ContactPageAdminView, ContactSubmissionAdminView, ContactSubmissionDetailAdminView
)

urlpatterns = [
    # Public
    path('layout/', LayoutPublicView.as_view(), name='layout'),
    path('about/', AboutPagePublicView.as_view(), name='about'),
    path('contact/', ContactPagePublicView.as_view(), name='contact'),
    path('disclosure/', PublicDisclosureView.as_view(), name='disclosure'),
    path('facilities/', FacilitiesPublicView.as_view(), name='facilities'),
    path('facilities/<slug:slug>/', FacilityDetailPublicView.as_view(), name='facility-detail'),
    path('seo/<slug:slug>/', PageSEOPublicView.as_view(), name='page-seo'),
    
    # Admin (Example routes - you might want to group these differently or put them in specific admin URLs)
    path('admin/settings/', SiteSettingsAdminView.as_view(), name='admin-settings'),
    path('admin/vision-mission/', VisionMissionAdminView.as_view(), name='admin-vision-mission'),
    path('admin/principal/', PrincipalMessageAdminView.as_view(), name='admin-principal'),
    path('admin/principal/reset/', PrincipalMessageResetView.as_view(), name='admin-principal-reset'),
    path('admin/about/', AboutPageAdminView.as_view(), name='admin-about-page'),
    path('admin/timeline/', TimelineEventAdminView.as_view(), name='admin-timeline'),
    path('admin/timeline/<int:pk>/', TimelineEventDetailAdminView.as_view(), name='admin-timeline-detail'),
    path('admin/management/', ManagementMemberAdminView.as_view(), name='admin-management'),
    path('admin/management/<int:pk>/', ManagementMemberDetailAdminView.as_view(), name='admin-management-detail'),
    path('admin/contact/', ContactPageAdminView.as_view(), name='admin-contact-page'),
    path('admin/messages/', ContactSubmissionAdminView.as_view(), name='admin-messages'),
    path('admin/messages/<int:pk>/', ContactSubmissionDetailAdminView.as_view(), name='admin-messages-detail'),
    path('admin/quick-links/', QuickLinkAdminView.as_view(), name='admin-quick-links'),
    path('admin/quick-links/<int:pk>/', QuickLinkDetailAdminView.as_view(), name='admin-quick-links-detail'),
    
    # Facilities
    path('admin/facilities/', FacilityAdminView.as_view(), name='admin-facilities'),
    path('admin/facilities/<int:pk>/', FacilityDetailAdminView.as_view(), name='admin-facilities-detail'),
    path('admin/facilities/<int:pk>/images/', FacilityGalleryAdminView.as_view(), name='admin-facilities-gallery'),
    path('admin/facility-images/<int:pk>/', FacilityImageDetailAdminView.as_view(), name='admin-facility-images-detail'),
    
    # Testimonials
    path('admin/testimonials/', TestimonialAdminView.as_view(), name='admin-testimonials'),
    path('admin/testimonials/<int:pk>/', TestimonialDetailAdminView.as_view(), name='admin-testimonials-detail'),
    
    # Achievements
    path('admin/achievements/', AchievementAdminView.as_view(), name='admin-achievements'),
    path('admin/achievements/<int:pk>/', AchievementDetailAdminView.as_view(), name='admin-achievements-detail'),
    
    # Disclosure
    path('admin/general-info/', GeneralInfoAdminView.as_view(), name='admin-general-info'),
    path('admin/general-info/<int:pk>/', GeneralInfoDetailAdminView.as_view(), name='admin-general-info-detail'),
    
    path('admin/infrastructure/', InfrastructureAdminView.as_view(), name='admin-infrastructure'),
    path('admin/infrastructure/<int:pk>/', InfrastructureDetailAdminView.as_view(), name='admin-infrastructure-detail'),
    
    path('admin/results/', ResultsAdminView.as_view(), name='admin-results'),
    path('admin/results/<int:pk>/', ResultsDetailAdminView.as_view(), name='admin-results-detail'),
    
    path('admin/fees/', FeesAdminView.as_view(), name='admin-fees'),
    path('admin/fees/<int:pk>/', FeesDetailAdminView.as_view(), name='admin-fees-detail'),
    
    path('admin/documents/', DocumentationAdminView.as_view(), name='admin-documents'),
    path('admin/documents/<int:pk>/', DocumentationDetailAdminView.as_view(), name='admin-documents-detail'),
    
    path('admin/seo/', PageSEOAdminView.as_view(), name='admin-seo'),
    path('admin/seo/<int:pk>/', PageSEODetailAdminView.as_view(), name='admin-seo-detail'),
]
