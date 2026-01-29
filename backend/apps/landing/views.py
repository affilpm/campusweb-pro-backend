from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .models import HeroSection, HomeAboutSection, AcademicHighlight
from .serializers import (
    HeroSectionPublicSerializer, HeroSectionAdminSerializer,
    HomeAboutPublicSerializer, HomeAboutAdminSerializer, 
    AcademicHighlightAdminSerializer
)
from rest_framework import status
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.views.generic import TemplateView

# Import models from other apps
from apps.school_info.models import (
    SiteSettings, AboutPage, PrincipalMessage, Facility, 
    GeneralInfo, Testimonial, Achievement
)
from apps.communication.models import Notice, Event
from apps.academics.models import AcademicsPage
from apps.gallery.models import GalleryImage
from apps.admissions.models import AdmissionSettings

# Import serializers
from apps.school_info.serializers import (
    SiteSettingsPublicSerializer, AboutPagePublicSerializer, 
    PrincipalMessagePublicSerializer, FacilityPublicSerializer,
    GeneralInfoPublicSerializer, TestimonialPublicSerializer, 
    AchievementPublicSerializer
)
from apps.communication.serializers import NoticePublicSerializer, EventPublicSerializer
from apps.academics.serializers import AcademicsPagePublicSerializer
from apps.gallery.serializers import GalleryImagePublicSerializer
from apps.admissions.serializers import AdmissionSettingsPublicSerializer

class HomeView(TemplateView):
    template_name = "landing/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Load all data for the homepage directly from ORM
        context['hero'] = HeroSection.load()
        context['about'] = HomeAboutSection.load()
        context['principal'] = PrincipalMessage.load()
        context['notices'] = Notice.objects.filter(status='published').order_by('-is_important', '-publish_date')[:5]
        context['events'] = Event.objects.filter(status='published').order_by('event_date')[:3]
        context['gallery'] = GalleryImage.objects.filter(is_featured=True).order_by('-created_at')[:6]
        context['facilities'] = Facility.objects.filter(is_active=True).order_by('order')
        context['achievements'] = Achievement.objects.filter(is_active=True).order_by('order')
        context['testimonials'] = Testimonial.objects.filter(is_active=True).order_by('order')
        context['admission_settings'] = AdmissionSettings.load()
        
        return context

class LandingHomeView(APIView):
    """
    GET /api/v1/landing/home/
    Aggregates data for the homepage
    """
    permission_classes = [AllowAny]

    def get(self, request):
        # 1. Site Settings
        site_settings = SiteSettings.load()
        
        # 2. Hero Section
        hero = HeroSection.load()
        
        # 3. About Preview
        about = HomeAboutSection.load()
        
        # 4. Principal Message
        principal = PrincipalMessage.load()
        
        # 5. Notices (Latest 5 published)
        notices = Notice.objects.filter(status='published').order_by('-is_important', '-publish_date')[:5]
        
        # 6. Events (Upcoming 3 published)
        events = Event.objects.filter(status='published').order_by('event_date')[:3]
        
        # 7. Gallery (Featured images)
        gallery = GalleryImage.objects.filter(is_featured=True).order_by('-created_at')[:6]
        
        # 8. Facilities (All active, ordered)
        facilities = Facility.objects.filter(is_active=True).order_by('order')
        
        # 9. Academics Scatistics (Homepage Stats)
        academic_stats = AcademicHighlight.objects.filter(is_active=True).order_by('order')

        # 10. Achievements
        achievements = Achievement.objects.filter(is_active=True).order_by('order')
        
        # 11. Testimonials
        testimonials = Testimonial.objects.filter(is_active=True).order_by('order')
        
        # 12. General Info (Public Disclosure preview)
        general_info = GeneralInfo.objects.filter(is_active=True)
        
        # 13. Admissions Status
        admission = AdmissionSettings.load()

        # 14. Results & Academics (Documents)
        from apps.school_info.models import ResultsAcademics
        from apps.school_info.serializers import ResultsAcademicsPublicSerializer
        results_docs = ResultsAcademics.objects.filter(is_active=True).order_by('order')
 
        data = {
            'site_settings': SiteSettingsPublicSerializer(site_settings, context={'request': request}).data,
            'hero': HeroSectionPublicSerializer(hero, context={'request': request}).data,
            'about': HomeAboutPublicSerializer(about, context={'request': request}).data,
            'principal': PrincipalMessagePublicSerializer(principal, context={'request': request}).data,
            'notices': NoticePublicSerializer(notices, many=True, context={'request': request}).data,
            'events': EventPublicSerializer(events, many=True, context={'request': request}).data,
            'gallery': GalleryImagePublicSerializer(gallery, many=True, context={'request': request}).data,
            'facilities': FacilityPublicSerializer(facilities, many=True, context={'request': request}).data,
            'academics': AcademicHighlightAdminSerializer(academic_stats, many=True, context={'request': request}).data, # Stats
            'results_academics': ResultsAcademicsPublicSerializer(results_docs, many=True, context={'request': request}).data, # Docs
            'achievements': AchievementPublicSerializer(achievements, many=True, context={'request': request}).data,
            'testimonials': TestimonialPublicSerializer(testimonials, many=True, context={'request': request}).data,
            'general_info': GeneralInfoPublicSerializer(general_info, many=True, context={'request': request}).data,
            'admission': AdmissionSettingsPublicSerializer(admission, context={'request': request}).data,
        }
        
        return Response(data)

# Admin Views

class HeroAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get(self, request):
        hero = HeroSection.load()
        return Response(HeroSectionAdminSerializer(hero, context={'request': request}).data)
        
    def put(self, request):
        hero = HeroSection.load()
        serializer = HeroSectionAdminSerializer(hero, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        return self.put(request)

class HomeAboutAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get(self, request):
        section = HomeAboutSection.load()
        return Response(HomeAboutAdminSerializer(section, context={'request': request}).data)
        
    def put(self, request):
        section = HomeAboutSection.load()
        serializer = HomeAboutAdminSerializer(section, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        return self.put(request)

class AcademicHighlightAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        items = AcademicHighlight.objects.all().order_by('order')
        return Response(AcademicHighlightAdminSerializer(items, many=True, context={'request': request}).data)
        
    def post(self, request):
        serializer = AcademicHighlightAdminSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AcademicHighlightDetailAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get_object(self, pk):
        try:
            return AcademicHighlight.objects.get(pk=pk)
        except AcademicHighlight.DoesNotExist:
            return None

    def put(self, request, pk):
        item = self.get_object(pk)
        if not item:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AcademicHighlightAdminSerializer(item, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        return self.put(request, pk)
        
    def delete(self, request, pk):
        item = self.get_object(pk)
        if not item:
            return Response(status=status.HTTP_404_NOT_FOUND)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
