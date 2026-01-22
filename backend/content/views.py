"""
Content app views.
Consolidated views from separate feature apps.
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.utils import timezone

from authentication.permissions import IsAdminUser
from .models import (
    SiteSettings, HeroSection, VisionMission, HomeAboutSection, PrincipalMessage, QuickLink,
    Notice, Event, GalleryCategory, GalleryImage, Facility, FacilityImage,
    Achievement, Testimonial, Documentation,
    AcademicHighlight, ClassCategory, Subject, AcademicsPage,
    AdmissionSettings, AdmissionStep,
    AboutPage, TimelineEvent, ManagementMember,
    GeneralInfo, ResultsAcademics, Infrastructure, Fees,
    PageSEO, ContactPage, ContactSubmission
)
from .serializers import (
    SiteSettingsPublicSerializer, HeroSectionPublicSerializer, VisionMissionPublicSerializer,
    HomeAboutSectionPublicSerializer, PrincipalMessagePublicSerializer, QuickLinkPublicSerializer,
    SiteSettingsAdminSerializer, HeroSectionAdminSerializer, VisionMissionAdminSerializer,
    HomeAboutSectionAdminSerializer, PrincipalMessageAdminSerializer, QuickLinkAdminSerializer,
    
    NoticePublicSerializer, NoticeAdminSerializer,
    EventPublicSerializer, EventListPublicSerializer, EventAdminSerializer,
    GalleryCategoryPublicSerializer, GalleryImagePublicSerializer, GalleryCategoryAdminSerializer, GalleryImageAdminSerializer,
    FacilityPublicSerializer, FacilityDetailSerializer, FacilityAdminSerializer, FacilityImageAdminSerializer,
    AchievementPublicSerializer, AchievementAdminSerializer,
    TestimonialPublicSerializer, TestimonialAdminSerializer,
    DocumentationPublicSerializer, DocumentationAdminSerializer,
    
    AcademicHighlightPublicSerializer, SubjectPublicSerializer, ClassCategoryPublicSerializer, AcademicsPagePublicSerializer,
    AcademicHighlightAdminSerializer, SubjectAdminSerializer, ClassCategoryAdminSerializer, AcademicsPageAdminSerializer,
    
    AdmissionSettingsPublicSerializer, AdmissionStepPublicSerializer,
    AdmissionSettingsAdminSerializer, AdmissionStepAdminSerializer,
    AdmissionStatusSerializer,
    
    AboutPagePublicSerializer, TimelineEventPublicSerializer, ManagementMemberPublicSerializer,
    AboutPageAdminSerializer, TimelineEventAdminSerializer, ManagementMemberAdminSerializer,
    
    GeneralInfoPublicSerializer, ResultsAcademicsPublicSerializer, InfrastructurePublicSerializer, FeesPublicSerializer,
    GeneralInfoAdminSerializer, ResultsAcademicsAdminSerializer, InfrastructureAdminSerializer, FeesAdminSerializer,
    
    PageSEOPublicSerializer, PageSEOAdminSerializer,
    
    ContactPagePublicSerializer, ContactSubmissionSerializer,
    ContactPageAdminSerializer, ContactSubmissionAdminSerializer
)


# ==================== HOMEPAGE VIEW ====================

class HomepagePublicView(APIView):
    """
    GET /api/public/home/
    Returns all homepage data in a single request.
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        context = {'request': request}
        
        # Get singleton data
        site_settings = SiteSettings.load()
        hero = HeroSection.load()
        about = HomeAboutSection.load()
        principal = PrincipalMessage.load()
        vision_mission = VisionMission.load()
        admission = AdmissionSettings.load()
        
        # Get list data
        notices = Notice.objects.filter(
            status='published',
            publish_date__lte=timezone.now().date()
        ).exclude(
            expiry_date__lt=timezone.now().date()
        )[:5]
        
        events = Event.objects.filter(status='published')[:6]
        gallery = GalleryImage.objects.filter(is_featured=True)[:8]
        facilities = Facility.objects.filter(is_active=True)
        academics = AcademicHighlight.objects.filter(is_active=True)
        achievements = Achievement.objects.filter(is_active=True).order_by('order')[:6]
        testimonials = Testimonial.objects.filter(is_active=True)[:4]
        quick_links = QuickLink.objects.filter(is_active=True)
        general_info = GeneralInfo.objects.filter(is_active=True).order_by('order', 'id')
        
        data = {
            'site_settings': SiteSettingsPublicSerializer(site_settings, context=context).data,
            'hero': HeroSectionPublicSerializer(hero, context=context).data,
            'about': HomeAboutSectionPublicSerializer(about, context=context).data,
            'principal': PrincipalMessagePublicSerializer(principal, context=context).data,
            'vision_mission': VisionMissionPublicSerializer(vision_mission, context=context).data,
            'admission': AdmissionStatusSerializer(admission, context=context).data,
            'notices': NoticePublicSerializer(notices, many=True, context=context).data,
            'events': EventListPublicSerializer(events, many=True, context=context).data,
            'gallery': GalleryImagePublicSerializer(gallery, many=True, context=context).data,
            'facilities': FacilityPublicSerializer(facilities, many=True, context=context).data,
            'academics': AcademicHighlightPublicSerializer(academics, many=True, context=context).data,
            'achievements': AchievementPublicSerializer(achievements, many=True, context=context).data,
            'testimonials': TestimonialPublicSerializer(testimonials, many=True, context=context).data,
            'quick_links': QuickLinkPublicSerializer(quick_links, many=True, context=context).data,
            'general_info': GeneralInfoPublicSerializer(general_info, many=True, context=context).data,
        }
        
        return Response(data)


class LayoutPublicView(APIView):
    """
    GET /api/public/layout/
    Returns only data needed for Global Layout (Header/Footer):
    - Site Settings (Logo, Name, Contact info)
    - Quick Links (Footer links)
    
    Lighter alternative to HomepagePublicView for inner pages.
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        context = {'request': request}
        
        site_settings = SiteSettings.load()
        quick_links = QuickLink.objects.filter(is_active=True)
        
        data = {
            'site_settings': SiteSettingsPublicSerializer(site_settings, context=context).data,
            'quick_links': QuickLinkPublicSerializer(quick_links, many=True, context=context).data,
        }
        
        return Response(data)


# ==================== SCHOOLS / SITE SETTINGS VIEWS ====================

# Admin
class SiteSettingsAdminView(APIView):
    """GET/PUT /api/admin/content/settings/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get(self, request):
        settings = SiteSettings.load()
        serializer = SiteSettingsAdminSerializer(settings, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request):
        settings = SiteSettings.load()
        serializer = SiteSettingsAdminSerializer(settings, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HeroSectionAdminView(APIView):
    """GET/PUT /api/admin/content/hero/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get(self, request):
        hero = HeroSection.load()
        serializer = HeroSectionAdminSerializer(hero, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request):
        hero = HeroSection.load()
        serializer = HeroSectionAdminSerializer(hero, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VisionMissionAdminView(APIView):
    """GET/PUT /api/admin/content/vision-mission/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        vm = VisionMission.load()
        serializer = VisionMissionAdminSerializer(vm, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request):
        vm = VisionMission.load()
        serializer = VisionMissionAdminSerializer(vm, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VisionMissionResetView(APIView):
    """POST /api/admin/content/vision-mission/reset/ - Reset specific sections"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def post(self, request):
        section = request.data.get('section')
        if not section:
            return Response({'error': 'Section parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        
        vm = VisionMission.load()
        
        section_fields = {
            'vision': {'vision_title': '', 'vision_content': ''},
            'mission': {'mission_title': '', 'mission_content': ''},
            'values': {'values_title': '', 'values_content': ''},
        }
        
        if section not in section_fields:
            return Response({'error': f'Invalid section: {section}'}, status=status.HTTP_400_BAD_REQUEST)
        
        for field, value in section_fields[section].items():
            setattr(vm, field, value)
        
        vm.save()
        
        serializer = VisionMissionAdminSerializer(vm, context={'request': request})
        return Response({
            'message': f'{section.title()} section reset successfully',
            'data': serializer.data
        })

class HomeAboutSectionAdminView(APIView):
    """GET/PUT /api/admin/content/home-about/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get(self, request):
        about = HomeAboutSection.load()
        serializer = HomeAboutSectionAdminSerializer(about, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request):
        about = HomeAboutSection.load()
        serializer = HomeAboutSectionAdminSerializer(about, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PrincipalMessageAdminView(APIView):
    """GET/PUT /api/admin/content/principal/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get(self, request):
        principal = PrincipalMessage.load()
        serializer = PrincipalMessageAdminSerializer(principal, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request):
        principal = PrincipalMessage.load()
        serializer = PrincipalMessageAdminSerializer(principal, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PrincipalMessageResetView(APIView):
    """POST /api/admin/content/principal/reset/ - Reset principal section"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def post(self, request):
        principal = PrincipalMessage.load()
        
        # Reset all fields
        principal.name = ''
        principal.title = ''
        principal.qualification = ''
        principal.message = ''
        principal.photo = None
        principal.save()
        
        serializer = PrincipalMessageAdminSerializer(principal, context={'request': request})
        return Response({
            'message': 'Principal section reset successfully',
            'data': serializer.data
        })

class QuickLinksAdminListCreateView(ListCreateAPIView):
    """GET/POST /api/admin/content/quick-links/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = QuickLinkAdminSerializer
    queryset = QuickLink.objects.all()

class QuickLinksAdminDetailView(RetrieveUpdateDestroyAPIView):
    """GET/PUT/DELETE /api/admin/content/quick-links/<id>/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = QuickLinkAdminSerializer
    queryset = QuickLink.objects.all()


# ==================== NOTICES VIEWS ====================

class NoticesPublicListView(ListAPIView):
    """GET /api/public/notices/
    
    Supports pagination via ?page=1 query param (20 items per page).
    Returns notices ordered by publish_date (newest first).
    """
    permission_classes = [AllowAny]
    serializer_class = NoticePublicSerializer
    
    def get_queryset(self):
        return Notice.objects.filter(
            status='published',
            publish_date__lte=timezone.now().date()
        ).exclude(
            expiry_date__lt=timezone.now().date()
        ).order_by('-publish_date', '-id')
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        # Pagination: limit to 20 items per page for mobile performance
        page = request.query_params.get('page', None)
        limit = 20
        
        if page:
            try:
                page_num = int(page)
                offset = (page_num - 1) * limit
                queryset = queryset[offset:offset + limit]
            except (ValueError, TypeError):
                pass
        else:
            # Default: return first 30 notices if no pagination requested
            queryset = queryset[:30]
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class NoticesPublicDetailView(RetrieveAPIView):
    """GET /api/public/notices/<pk>/"""
    permission_classes = [AllowAny]
    serializer_class = NoticePublicSerializer
    queryset = Notice.objects.filter(status='published')

# Admin
class NoticesAdminListCreateView(ListCreateAPIView):
    """GET/POST /api/admin/content/notices/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = NoticeAdminSerializer
    queryset = Notice.objects.all()

class NoticesAdminDetailView(RetrieveUpdateDestroyAPIView):
    """GET/PUT/DELETE /api/admin/content/notices/<id>/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = NoticeAdminSerializer
    queryset = Notice.objects.all()


# ==================== EVENTS VIEWS ====================

class EventsPublicListView(ListAPIView):
    """GET /api/public/events/"""
    permission_classes = [AllowAny]
    serializer_class = EventListPublicSerializer
    queryset = Event.objects.filter(status='published')

class EventPublicDetailView(RetrieveAPIView):
    """GET /api/public/events/<slug>/"""
    permission_classes = [AllowAny]
    serializer_class = EventPublicSerializer
    lookup_field = 'slug'
    queryset = Event.objects.filter(status='published')

# Admin
class EventsAdminListCreateView(ListCreateAPIView):
    """GET/POST /api/admin/content/events/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = EventAdminSerializer
    queryset = Event.objects.all()

class EventsAdminDetailView(RetrieveUpdateDestroyAPIView):
    """GET/PUT/DELETE /api/admin/content/events/<id>/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = EventAdminSerializer
    queryset = Event.objects.all()


# ==================== GALLERY VIEWS ====================

class GalleryPublicView(APIView):
    """GET /api/public/gallery/"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        context = {'request': request}
        categories = list(GalleryCategoryPublicSerializer(GalleryCategory.objects.all(), many=True).data)
        gallery_qs = GalleryImage.objects.select_related('category').all()
        category_slug = request.query_params.get('category')
        if category_slug and category_slug != 'all':
            gallery_qs = gallery_qs.filter(category__slug=category_slug)
            
        # Pagination
        try:
            page = int(request.query_params.get('page', 1))
            limit = int(request.query_params.get('limit', 50))
            if limit > 100: limit = 100 # Max limit
        except (ValueError, TypeError):
            page = 1
            limit = 50
            
        offset = (page - 1) * limit
        
        # Slicing
        gallery_qs = gallery_qs.order_by('-id') # Ensure ordering
        images_list = gallery_qs[offset:offset + limit]

        images_data = list(GalleryImagePublicSerializer(images_list, many=True, context=context).data)
        
        return Response({
            'categories': categories,
            'images': images_data,
        })

# Admin
class GalleryCategoriesAdminListCreateView(ListCreateAPIView):
    """GET/POST /api/admin/content/gallery/categories/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = GalleryCategoryAdminSerializer
    queryset = GalleryCategory.objects.all()

class GalleryCategoriesAdminDetailView(RetrieveUpdateDestroyAPIView):
    """GET/PUT/DELETE /api/admin/content/gallery/categories/<id>/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = GalleryCategoryAdminSerializer
    queryset = GalleryCategory.objects.all()

class GalleryImagesAdminListCreateView(ListCreateAPIView):
    """GET/POST /api/admin/content/gallery/images/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = GalleryImageAdminSerializer
    queryset = GalleryImage.objects.select_related('category').all()

class GalleryImagesAdminDetailView(RetrieveUpdateDestroyAPIView):
    """GET/PUT/DELETE /api/admin/content/gallery/images/<id>/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = GalleryImageAdminSerializer
    queryset = GalleryImage.objects.all()


# ==================== FACILITIES VIEWS ====================

class FacilityPublicDetailView(APIView):
    """GET /api/public/facilities/<slug>/"""
    permission_classes = [AllowAny]

    def get(self, request, slug):
        try:
            facility = Facility.objects.get(slug=slug, is_active=True)
        except Facility.DoesNotExist:
            return Response({'error': 'Facility not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = FacilityDetailSerializer(facility, context={'request': request})
        return Response(serializer.data)

# Admin
class FacilitiesAdminListCreateView(ListCreateAPIView):
    """GET/POST /api/admin/content/facilities/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = FacilityAdminSerializer
    queryset = Facility.objects.prefetch_related('gallery_images').all()

class FacilitiesAdminDetailView(RetrieveUpdateDestroyAPIView):
    """GET/PUT/DELETE /api/admin/content/facilities/<id>/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = FacilityAdminSerializer
    queryset = Facility.objects.all()

class FacilityImagesAdminListCreateView(ListCreateAPIView):
    """GET/POST /api/admin/content/facilities/<id>/images/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = FacilityImageAdminSerializer

    def get_queryset(self):
        return FacilityImage.objects.select_related('facility').filter(facility_id=self.kwargs['facility_id'])

    def perform_create(self, serializer):
        serializer.save(facility_id=self.kwargs['facility_id'])

class FacilityImagesAdminDetailView(RetrieveUpdateDestroyAPIView):
    """GET/PUT/DELETE /api/admin/content/facility-images/<id>/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = FacilityImageAdminSerializer
    queryset = FacilityImage.objects.all()


# ==================== ACHIEVEMENTS VIEWS ====================

class AchievementAdminListCreateView(ListCreateAPIView):
    """GET/POST /api/admin/content/achievements/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = AchievementAdminSerializer
    queryset = Achievement.objects.all()

class AchievementAdminDetailView(RetrieveUpdateDestroyAPIView):
    """GET/PUT/DELETE /api/admin/content/achievements/<id>/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = AchievementAdminSerializer
    queryset = Achievement.objects.all()


# ==================== TESTIMONIALS VIEWS ====================

class TestimonialsAdminListCreateView(ListCreateAPIView):
    """GET/POST /api/admin/content/testimonials/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = TestimonialAdminSerializer
    queryset = Testimonial.objects.all()

class TestimonialsAdminDetailView(RetrieveUpdateDestroyAPIView):
    """GET/PUT/DELETE /api/admin/content/testimonials/<id>/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = TestimonialAdminSerializer
    queryset = Testimonial.objects.all()





class DocumentsPublicListView(ListAPIView):
    """GET /api/public/documents/ (Documentation)"""
    permission_classes = [AllowAny]
    serializer_class = DocumentationPublicSerializer
    queryset = Documentation.objects.filter(is_active=True).order_by('order', 'id')

class DocumentationAdminListCreateView(ListCreateAPIView):
    """GET/POST /api/admin/content/documentation/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = DocumentationAdminSerializer
    queryset = Documentation.objects.all().order_by('order', 'id')

class DocumentationAdminDetailView(RetrieveUpdateDestroyAPIView):
    """GET/PUT/DELETE /api/admin/content/documentation/<id>/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = DocumentationAdminSerializer
    queryset = Documentation.objects.all()


# ==================== ACADEMICS VIEWS ====================

class AcademicsPagePublicView(APIView):
    """GET /api/public/academics/"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        context = {'request': request}
        academics = AcademicsPage.load()
        site_settings = SiteSettings.load()
        quick_links = QuickLink.objects.filter(is_active=True)
        
        serializer = AcademicsPagePublicSerializer(academics, context=context)
        data = serializer.data
        data['site_settings'] = SiteSettingsPublicSerializer(site_settings, context=context).data
        data['quick_links'] = QuickLinkPublicSerializer(quick_links, many=True, context=context).data
        
        return Response(data)

# Admin
class AcademicsAdminListCreateView(ListCreateAPIView):
    """GET/POST /api/admin/content/academics/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = AcademicHighlightAdminSerializer
    queryset = AcademicHighlight.objects.all()

class AcademicsAdminDetailView(RetrieveUpdateDestroyAPIView):
    """GET/PUT/DELETE /api/admin/content/academics/<id>/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = AcademicHighlightAdminSerializer
    queryset = AcademicHighlight.objects.all()

class ClassCategoriesAdminListCreateView(ListCreateAPIView):
    """GET/POST /api/admin/content/academics/categories/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = ClassCategoryAdminSerializer
    queryset = ClassCategory.objects.all()

class ClassCategoriesAdminDetailView(RetrieveUpdateDestroyAPIView):
    """GET/PUT/DELETE /api/admin/content/academics/categories/<id>/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = ClassCategoryAdminSerializer
    queryset = ClassCategory.objects.all()

class SubjectsAdminListCreateView(ListCreateAPIView):
    """GET/POST /api/admin/content/academics/subjects/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = SubjectAdminSerializer
    queryset = Subject.objects.all()

class SubjectsAdminDetailView(RetrieveUpdateDestroyAPIView):
    """GET/PUT/DELETE /api/admin/content/academics/subjects/<id>/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = SubjectAdminSerializer
    queryset = Subject.objects.all()

class AcademicsPageAdminView(APIView):
    """GET/PUT /api/admin/content/academics/page/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get(self, request):
        academics = AcademicsPage.load()
        serializer = AcademicsPageAdminSerializer(academics, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request):
        academics = AcademicsPage.load()
        serializer = AcademicsPageAdminSerializer(academics, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ==================== ADMISSIONS VIEWS ====================

class AdmissionsPagePublicView(APIView):
    """GET /api/public/admissions/"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        context = {'request': request}
        admission = AdmissionSettings.load()
        site_settings = SiteSettings.load()
        quick_links = QuickLink.objects.filter(is_active=True)
        
        serializer = AdmissionSettingsPublicSerializer(admission, context=context)
        data = serializer.data
        data['site_settings'] = SiteSettingsPublicSerializer(site_settings, context=context).data
        data['quick_links'] = QuickLinkPublicSerializer(quick_links, many=True, context=context).data
        
        return Response(data)

# Admin
class AdmissionSettingsAdminView(APIView):
    """GET/PUT /api/admin/content/admissions/settings/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get(self, request):
        admission = AdmissionSettings.load()
        serializer = AdmissionSettingsAdminSerializer(admission, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request):
        admission = AdmissionSettings.load()
        serializer = AdmissionSettingsAdminSerializer(admission, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdmissionStepsAdminListCreateView(ListCreateAPIView):
    """GET/POST /api/admin/content/admissions/steps/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = AdmissionStepAdminSerializer
    queryset = AdmissionStep.objects.all()

class AdmissionStepsAdminDetailView(RetrieveUpdateDestroyAPIView):
    """GET/PUT/DELETE /api/admin/content/admissions/steps/<id>/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = AdmissionStepAdminSerializer
    queryset = AdmissionStep.objects.all()


# ==================== ABOUT PAGE VIEWS ====================

class AboutPagePublicView(APIView):
    """GET /api/public/about/"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        context = {'request': request}
        about = AboutPage.load()
        
        # Singleton data for header/footer
        site_settings = SiteSettings.load()
        quick_links = QuickLink.objects.filter(is_active=True)
        
        serializer = AboutPagePublicSerializer(about, context=context)
        data = serializer.data
        
        # Additional data for full About Page
        about_section = HomeAboutSection.load()
        principal = PrincipalMessage.load()
        vision_mission = VisionMission.load()
        facilities = Facility.objects.filter(is_active=True)
        
        data['site_settings'] = SiteSettingsPublicSerializer(site_settings, context=context).data
        data['quick_links'] = QuickLinkPublicSerializer(quick_links, many=True, context=context).data
        
        data['about_section'] = HomeAboutSectionPublicSerializer(about_section, context=context).data
        data['principal'] = PrincipalMessagePublicSerializer(principal, context=context).data
        data['vision_mission'] = VisionMissionPublicSerializer(vision_mission, context=context).data
        data['facilities'] = FacilityPublicSerializer(facilities, many=True, context=context).data
        
        # Attempt to get Affiliation Number from General Info
        affiliation_info = GeneralInfo.objects.filter(title__icontains='Affiliation', is_active=True).first()
        data['cbse_affiliation_no'] = affiliation_info.value if affiliation_info else ""
        
        return Response(data)


# Admin
class AboutPageAdminView(APIView):
    """GET/PUT /api/admin/content/about/page/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get(self, request):
        about = AboutPage.load()
        serializer = AboutPageAdminSerializer(about, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request):
        about = AboutPage.load()
        serializer = AboutPageAdminSerializer(about, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AboutPageResetView(APIView):
    """POST /api/admin/content/about/page/reset/ - Reset specific sections"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def post(self, request):
        section = request.data.get('section')
        if not section:
            return Response({'error': 'Section parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        
        about = AboutPage.load()
        
        # Define which fields to reset for each section
        section_fields = {
            'history': {
                'history_title': '',
                'history_content': '',
                'history_image': None,
            },
            'infrastructure': {
                'infrastructure_title': '',
                'infrastructure_content': '',
            },
            'hero': {
                'hero_title': '',
                'hero_subtitle': '',
            },
        }
        
        if section not in section_fields:
            return Response({'error': f'Invalid section: {section}'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Reset the fields
        for field, value in section_fields[section].items():
            setattr(about, field, value)
        
        about.save()
        
        serializer = AboutPageAdminSerializer(about, context={'request': request})
        return Response({
            'message': f'{section.title()} section reset successfully',
            'data': serializer.data
        })

class TimelineEventsAdminListCreateView(ListCreateAPIView):
    """GET/POST /api/admin/content/about/timeline/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = TimelineEventAdminSerializer
    queryset = TimelineEvent.objects.all().order_by('order', 'year')

class TimelineEventsAdminDetailView(RetrieveUpdateDestroyAPIView):
    """GET/PUT/DELETE /api/admin/content/about/timeline/<id>/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = TimelineEventAdminSerializer
    queryset = TimelineEvent.objects.all()

class ManagementMembersAdminListCreateView(ListCreateAPIView):
    """GET/POST /api/admin/content/about/management/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = ManagementMemberAdminSerializer
    queryset = ManagementMember.objects.all().order_by('order')

class ManagementMembersAdminDetailView(RetrieveUpdateDestroyAPIView):
    """GET/PUT/DELETE /api/admin/content/about/management/<id>/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = ManagementMemberAdminSerializer
    queryset = ManagementMember.objects.all()


# ==================== PUBLIC DISCLOSURE VIEWS ====================

class GeneralInfoPublicListView(ListAPIView):
    """GET /api/public/general-info/"""
    permission_classes = [AllowAny]
    serializer_class = GeneralInfoPublicSerializer
    queryset = GeneralInfo.objects.filter(is_active=True).order_by('order', 'id')

class ResultsAcademicsPublicListView(ListAPIView):
    """GET /api/public/results-academics/"""
    permission_classes = [AllowAny]
    serializer_class = ResultsAcademicsPublicSerializer
    queryset = ResultsAcademics.objects.filter(is_active=True).order_by('order', 'id')

class InfrastructurePublicListView(ListAPIView):
    """GET /api/public/infrastructure/"""
    permission_classes = [AllowAny]
    serializer_class = InfrastructurePublicSerializer
    queryset = Infrastructure.objects.filter(is_active=True).order_by('order', 'id')

class FeesPublicListView(ListAPIView):
    """GET /api/public/fees/"""
    permission_classes = [AllowAny]
    serializer_class = FeesPublicSerializer
    queryset = Fees.objects.filter(is_active=True).order_by('order', 'id')



class GeneralInfoAdminListCreateView(ListCreateAPIView):
    """GET/POST /api/admin/content/general-info/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = GeneralInfoAdminSerializer
    queryset = GeneralInfo.objects.all().order_by('order', 'id')

class GeneralInfoAdminDetailView(RetrieveUpdateDestroyAPIView):
    """GET/PUT/DELETE /api/admin/content/general-info/<id>/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = GeneralInfoAdminSerializer
    queryset = GeneralInfo.objects.all()

class ResultsAcademicsAdminListCreateView(ListCreateAPIView):
    """GET/POST /api/admin/content/results-academics/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = ResultsAcademicsAdminSerializer
    queryset = ResultsAcademics.objects.all().order_by('order', 'id')

class ResultsAcademicsAdminDetailView(RetrieveUpdateDestroyAPIView):
    """GET/PUT/DELETE /api/admin/content/results-academics/<id>/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = ResultsAcademicsAdminSerializer
    queryset = ResultsAcademics.objects.all()

class InfrastructureAdminListCreateView(ListCreateAPIView):
    """GET/POST /api/admin/content/infrastructure/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = InfrastructureAdminSerializer
    queryset = Infrastructure.objects.all().order_by('order', 'id')

class InfrastructureAdminDetailView(RetrieveUpdateDestroyAPIView):
    """GET/PUT/DELETE /api/admin/content/infrastructure/<id>/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = InfrastructureAdminSerializer
    queryset = Infrastructure.objects.all()

class FeesAdminListCreateView(ListCreateAPIView):
    """GET/POST /api/admin/content/fees/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = FeesAdminSerializer
    queryset = Fees.objects.all().order_by('order', 'id')

class FeesAdminDetailView(RetrieveUpdateDestroyAPIView):
    """GET/PUT/DELETE /api/admin/content/fees/<id>/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = FeesAdminSerializer
    queryset = Fees.objects.all()


# ==================== SEO VIEWS ====================

class PageSEOPublicView(APIView):
    """GET /api/public/seo/<page_slug>/"""
    permission_classes = [AllowAny]
    
    def get(self, request, page_slug):
        try:
            seo = PageSEO.objects.get(page_slug=page_slug)
            serializer = PageSEOPublicSerializer(seo, context={'request': request})
            return Response(serializer.data)
        except PageSEO.DoesNotExist:
            return Response({
                'page_slug': page_slug,
                'title': '',
                'meta_description': '',
                'meta_keywords': '',
                'og_image': None
            })

class PageSEOAdminListCreateView(ListCreateAPIView):
    """GET/POST /api/admin/content/seo/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = PageSEOAdminSerializer
    queryset = PageSEO.objects.all()

class PageSEOAdminDetailView(RetrieveUpdateDestroyAPIView):
    """GET/PUT/DELETE /api/admin/content/seo/<id>/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = PageSEOAdminSerializer
    queryset = PageSEO.objects.all()


# ==================== CONTACT VIEWS ====================

class ContactPagePublicView(APIView):
    """GET /api/public/contact/"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        context = {'request': request}
        contact_page = ContactPage.load()
        
        # Get global data
        site_settings = SiteSettings.load()
        quick_links = QuickLink.objects.filter(is_active=True)
        
        serializer = ContactPagePublicSerializer(contact_page, context=context)
        data = serializer.data
        
        # Inject global data
        data['site_settings'] = SiteSettingsPublicSerializer(site_settings, context=context).data
        data['quick_links'] = QuickLinkPublicSerializer(quick_links, many=True, context=context).data
        
        return Response(data)

class ContactSubmissionView(APIView):
    """POST /api/public/contact/submit/"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = ContactSubmissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Your message has been sent successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Admin
class ContactPageAdminView(APIView):
    """GET/PUT /api/admin/content/contact/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        contact = ContactPage.load()
        serializer = ContactPageAdminSerializer(contact, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request):
        contact = ContactPage.load()
        serializer = ContactPageAdminSerializer(contact, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ContactSubmissionsAdminListView(ListAPIView):
    """GET /api/admin/content/contact/submissions/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ContactSubmissionAdminSerializer
    queryset = ContactSubmission.objects.all()

class ContactSubmissionsAdminDetailView(RetrieveUpdateDestroyAPIView):
    """GET/PUT/DELETE /api/admin/content/contact/submissions/<id>/"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ContactSubmissionAdminSerializer
    queryset = ContactSubmission.objects.all()
