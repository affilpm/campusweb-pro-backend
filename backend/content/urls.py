"""
Content app URLs.
Consolidated URLs from separate feature apps.
"""

from django.urls import path
from .views import (
    # Homepage
    HomepagePublicView,
    
    # Schools / Site Settings
    SiteSettingsAdminView, HeroSectionAdminView,
    VisionMissionAdminView, VisionMissionResetView, HomeAboutSectionAdminView,
    PrincipalMessageAdminView, PrincipalMessageResetView, QuickLinksAdminListCreateView, QuickLinksAdminDetailView,
    
    # Notices
    NoticesPublicListView, NoticesPublicDetailView,
    NoticesAdminListCreateView, NoticesAdminDetailView,
    
    # Events
    EventsPublicListView, EventPublicDetailView,
    EventsAdminListCreateView, EventsAdminDetailView,
    
    # Gallery
    GalleryPublicView,
    GalleryCategoriesAdminListCreateView, GalleryCategoriesAdminDetailView,
    GalleryImagesAdminListCreateView, GalleryImagesAdminDetailView,
    
    # Facilities
    FacilityPublicDetailView,
    FacilitiesAdminListCreateView, FacilitiesAdminDetailView,
    FacilityImagesAdminListCreateView, FacilityImagesAdminDetailView,
    
    # Achievements
    AchievementAdminListCreateView, AchievementAdminDetailView,
    
    # Testimonials
    TestimonialsAdminListCreateView, TestimonialsAdminDetailView,
    
    # Downloads
    DownloadsPublicListView, DeclarationsPublicListView,
    DownloadsAdminListCreateView, DownloadsAdminDetailView,
    DocumentationAdminListCreateView, DocumentationAdminDetailView,
    
    # Academics
    AcademicsPagePublicView,
    AcademicsAdminListCreateView, AcademicsAdminDetailView,
    ClassCategoriesAdminListCreateView, ClassCategoriesAdminDetailView,
    SubjectsAdminListCreateView, SubjectsAdminDetailView,
    AcademicsPageAdminView,
    
    # Admissions
    AdmissionsPagePublicView,
    AdmissionSettingsAdminView,
    AdmissionStepsAdminListCreateView, AdmissionStepsAdminDetailView,
    
    # About
    AboutPagePublicView,
    AboutPageAdminView, AboutPageResetView,
    TimelineEventsAdminListCreateView, TimelineEventsAdminDetailView,
    ManagementMembersAdminListCreateView, ManagementMembersAdminDetailView,
    
    # Public Disclosure
    GeneralInfoAdminListCreateView, GeneralInfoAdminDetailView,
    ResultsAcademicsAdminListCreateView, ResultsAcademicsAdminDetailView,
    InfrastructureAdminListCreateView, InfrastructureAdminDetailView,
    FeesAdminListCreateView, FeesAdminDetailView,
    
    # Public Disclosure Public
    GeneralInfoPublicListView, ResultsAcademicsPublicListView,
    InfrastructurePublicListView, FeesPublicListView,
    
    # SEO
    PageSEOPublicView,
    PageSEOAdminListCreateView, PageSEOAdminDetailView,
    
    # Contact
    ContactPagePublicView, ContactSubmissionView,
    ContactPageAdminView,
    ContactSubmissionsAdminListView, ContactSubmissionsAdminDetailView,
)

app_name = 'content'

urlpatterns = [
    # ==================== PUBLIC URLS ====================
    # Start with public/ to match previous structure likely expected by frontend public pages
    
    # Homepage
    path('public/home/', HomepagePublicView.as_view(), name='public-home'),
    
    # Notices
    path('public/notices/', NoticesPublicListView.as_view(), name='public-notices-list'),
    path('public/notices/<int:pk>/', NoticesPublicDetailView.as_view(), name='public-notices-detail'),
    
    # Events
    path('public/events/', EventsPublicListView.as_view(), name='public-events-list'),
    path('public/events/<slug:slug>/', EventPublicDetailView.as_view(), name='public-events-detail'),
    
    # Gallery
    path('public/gallery/', GalleryPublicView.as_view(), name='public-gallery'),
    
    # Facilities
    path('public/facilities/<slug:slug>/', FacilityPublicDetailView.as_view(), name='public-facilities-detail'),
    
    # Downloads
    path('public/downloads/', DownloadsPublicListView.as_view(), name='public-downloads'),
    path('public/declarations/', DeclarationsPublicListView.as_view(), name='public-declarations'),
    path('public/documents/', DeclarationsPublicListView.as_view(), name='public-documents'), # Alias for frontend compatibility
    
    # Academics
    path('public/academics/', AcademicsPagePublicView.as_view(), name='public-academics'),
    
    # Admissions
    path('public/admissions/', AdmissionsPagePublicView.as_view(), name='public-admissions'),
    
    # About
    path('public/about/', AboutPagePublicView.as_view(), name='public-about'),
    
    # SEO
    path('public/seo/<slug:page_slug>/', PageSEOPublicView.as_view(), name='public-seo'),
    
    # Contact
    path('public/contact/', ContactPagePublicView.as_view(), name='public-contact'),
    path('public/contact/submit/', ContactSubmissionView.as_view(), name='public-contact-submit'),
    
    # Public Disclosure
    path('public/general-info/', GeneralInfoPublicListView.as_view(), name='public-general-info'),
    path('public/results-academics/', ResultsAcademicsPublicListView.as_view(), name='public-results-academics'),
    path('public/infrastructure/', InfrastructurePublicListView.as_view(), name='public-infrastructure'),
    path('public/fees/', FeesPublicListView.as_view(), name='public-fees'),
    
    
    # ==================== ADMIN URLS ====================
    # Prefix with admin/content/ to match legacy structure
    
    # Site Settings
    path('admin/content/settings/', SiteSettingsAdminView.as_view(), name='admin-site-settings'),
    path('admin/content/hero/', HeroSectionAdminView.as_view(), name='admin-hero'),
    path('admin/content/home-about/', HomeAboutSectionAdminView.as_view(), name='admin-home-about'),
    path('admin/content/principal/', PrincipalMessageAdminView.as_view(), name='admin-principal'),
    path('admin/content/principal/reset/', PrincipalMessageResetView.as_view(), name='admin-principal-reset'),
    path('admin/content/vision-mission/', VisionMissionAdminView.as_view(), name='admin-vision-mission'),
    path('admin/content/vision-mission/reset/', VisionMissionResetView.as_view(), name='admin-vision-mission-reset'),
    path('admin/content/quick-links/', QuickLinksAdminListCreateView.as_view(), name='admin-quick-links'),
    path('admin/content/quick-links/<int:pk>/', QuickLinksAdminDetailView.as_view(), name='admin-quick-link-detail'),
    
    # Notices
    path('admin/content/notices/', NoticesAdminListCreateView.as_view(), name='admin-notices-list'),
    path('admin/content/notices/<int:pk>/', NoticesAdminDetailView.as_view(), name='admin-notices-detail'),
    
    # Events
    path('admin/content/events/', EventsAdminListCreateView.as_view(), name='admin-events-list'),
    path('admin/content/events/<int:pk>/', EventsAdminDetailView.as_view(), name='admin-events-detail'),
    
    # Gallery
    path('admin/content/gallery/categories/', GalleryCategoriesAdminListCreateView.as_view(), name='admin-gallery-categories'),
    path('admin/content/gallery/categories/<int:pk>/', GalleryCategoriesAdminDetailView.as_view(), name='admin-gallery-category-detail'),
    path('admin/content/gallery/images/', GalleryImagesAdminListCreateView.as_view(), name='admin-gallery-images'),
    path('admin/content/gallery/images/<int:pk>/', GalleryImagesAdminDetailView.as_view(), name='admin-gallery-image-detail'),
    
    # Facilities
    path('admin/content/facilities/', FacilitiesAdminListCreateView.as_view(), name='admin-facilities-list'),
    path('admin/content/facilities/<int:pk>/', FacilitiesAdminDetailView.as_view(), name='admin-facilities-detail'),
    path('admin/content/facilities/<int:facility_id>/images/', FacilityImagesAdminListCreateView.as_view(), name='admin-facility-images-list'),
    path('admin/content/facility-images/<int:pk>/', FacilityImagesAdminDetailView.as_view(), name='admin-facility-image-detail'),
    
    # Achievements
    path('admin/content/achievements/', AchievementAdminListCreateView.as_view(), name='admin-achievements-list'),
    path('admin/content/achievements/<int:pk>/', AchievementAdminDetailView.as_view(), name='admin-achievements-detail'),
    
    # Testimonials
    path('admin/content/testimonials/', TestimonialsAdminListCreateView.as_view(), name='admin-testimonials-list'),
    path('admin/content/testimonials/<int:pk>/', TestimonialsAdminDetailView.as_view(), name='admin-testimonials-detail'),
    
    # Downloads
    path('admin/content/downloads/', DownloadsAdminListCreateView.as_view(), name='admin-downloads-list'),
    path('admin/content/downloads/<int:pk>/', DownloadsAdminDetailView.as_view(), name='admin-downloads-detail'),
    path('admin/content/documentation/', DocumentationAdminListCreateView.as_view(), name='admin-documentation-list'),
    path('admin/content/documentation/<int:pk>/', DocumentationAdminDetailView.as_view(), name='admin-documentation-detail'),
    
    # Academics
    path('admin/content/academics/', AcademicsAdminListCreateView.as_view(), name='admin-academics-list'),
    path('admin/content/academics/<int:pk>/', AcademicsAdminDetailView.as_view(), name='admin-academics-detail'),
    path('admin/content/academics/categories/', ClassCategoriesAdminListCreateView.as_view(), name='admin-class-categories'),
    path('admin/content/academics/categories/<int:pk>/', ClassCategoriesAdminDetailView.as_view(), name='admin-class-category-detail'),
    path('admin/content/academics/subjects/', SubjectsAdminListCreateView.as_view(), name='admin-subjects'),
    path('admin/content/academics/subjects/<int:pk>/', SubjectsAdminDetailView.as_view(), name='admin-subject-detail'),
    path('admin/content/academics/page/', AcademicsPageAdminView.as_view(), name='admin-academics-page'),
    
    # Admissions
    path('admin/content/admissions/settings/', AdmissionSettingsAdminView.as_view(), name='admin-admissions-settings'),
    path('admin/content/admissions/steps/', AdmissionStepsAdminListCreateView.as_view(), name='admin-admission-steps'),
    path('admin/content/admissions/steps/<int:pk>/', AdmissionStepsAdminDetailView.as_view(), name='admin-admission-step-detail'),
    
    # About
    path('admin/content/about/page/', AboutPageAdminView.as_view(), name='admin-about-page'),
    path('admin/content/about/page/reset/', AboutPageResetView.as_view(), name='admin-about-reset'),
    path('admin/content/about/timeline/', TimelineEventsAdminListCreateView.as_view(), name='admin-timeline'),
    path('admin/content/about/timeline/<int:pk>/', TimelineEventsAdminDetailView.as_view(), name='admin-timeline-detail'),
    path('admin/content/about/management/', ManagementMembersAdminListCreateView.as_view(), name='admin-management'),
    path('admin/content/about/management/<int:pk>/', ManagementMembersAdminDetailView.as_view(), name='admin-management-detail'),
    
    # Public Disclosure
    path('admin/content/general-info/', GeneralInfoAdminListCreateView.as_view(), name='admin-general-info'),
    path('admin/content/general-info/<int:pk>/', GeneralInfoAdminDetailView.as_view(), name='admin-general-info-detail'),
    path('admin/content/results-academics/', ResultsAcademicsAdminListCreateView.as_view(), name='admin-results'),
    path('admin/content/results-academics/<int:pk>/', ResultsAcademicsAdminDetailView.as_view(), name='admin-results-detail'),
    path('admin/content/infrastructure/', InfrastructureAdminListCreateView.as_view(), name='admin-infrastructure'),
    path('admin/content/infrastructure/<int:pk>/', InfrastructureAdminDetailView.as_view(), name='admin-infrastructure-detail'),
    path('admin/content/fees/', FeesAdminListCreateView.as_view(), name='admin-fees'),
    path('admin/content/fees/<int:pk>/', FeesAdminDetailView.as_view(), name='admin-fees-detail'),
    
    # SEO
    path('admin/content/seo/', PageSEOAdminListCreateView.as_view(), name='admin-seo'),
    path('admin/content/seo/<int:pk>/', PageSEOAdminDetailView.as_view(), name='admin-seo-detail'),
    
    # Contact
    path('admin/content/contact/', ContactPageAdminView.as_view(), name='admin-contact-page'),
    path('admin/content/contact/submissions/', ContactSubmissionsAdminListView.as_view(), name='admin-contact-submissions'),
    path('admin/content/contact/submissions/<int:pk>/', ContactSubmissionsAdminDetailView.as_view(), name='admin-contact-submission-detail'),
]
