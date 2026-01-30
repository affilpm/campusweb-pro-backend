from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.shortcuts import get_object_or_404

from .models import (
    SiteSettings, VisionMission, PrincipalMessage, QuickLink,
    AboutPage, TimelineEvent, ManagementMember,
    GeneralInfo, ResultsAcademics, Infrastructure, Fees,
    Documentation, PageSEO, ContactPage, ContactSubmission,
    Testimonial, Achievement, Facility, FacilityImage,
    TimelineEvent, ManagementMember
)
from apps.landing.models import HomeAboutSection
from apps.landing.serializers import HomeAboutPublicSerializer
from .serializers import (
    SiteSettingsPublicSerializer, SiteSettingsAdminSerializer,
    VisionMissionPublicSerializer, PrincipalMessagePublicSerializer,
    PrincipalMessageAdminSerializer,
    QuickLinkPublicSerializer,
    AboutPagePublicSerializer, TimelineEventPublicSerializer, ManagementMemberPublicSerializer,
    AboutPageAdminSerializer, TimelineEventAdminSerializer, ManagementMemberAdminSerializer,
    GeneralInfoPublicSerializer, ResultsAcademicsPublicSerializer, InfrastructurePublicSerializer, FeesPublicSerializer,
    DocumentationPublicSerializer,
    PageSEOPublicSerializer, PageSEOAdminSerializer,
    ContactPagePublicSerializer, ContactSubmissionSerializer,
    ContactPageAdminSerializer, ContactSubmissionAdminSerializer,
    FacilityImageCreateSerializer, FacilityImageReadSerializer, FacilityImageAdminSerializer,
    TestimonialPublicSerializer, AchievementPublicSerializer, FacilityPublicSerializer,
    FacilityAdminSerializer
)

# ==================== PUBLIC VIEWS ====================

class LayoutPublicView(APIView):
    """
    GET /api/public/layout/
    Returns only data needed for Global Layout (Header/Footer):
    - Site Settings (Logo, Name, Contact info)
    - Quick Links (Footer links)
    """
    permission_classes = [AllowAny]

    def get(self, request):
        settings = SiteSettings.load()
        quick_links = QuickLink.objects.filter(is_active=True).order_by('order')

        data = {
            'site_settings': SiteSettingsPublicSerializer(settings, context={'request': request}).data,
            'quick_links': QuickLinkPublicSerializer(quick_links, many=True, context={'request': request}).data,
        }
        return Response(data)

class AboutPagePublicView(APIView):
    """
    GET /api/public/about/
    """
    permission_classes = [AllowAny]

    def get(self, request):
        about_page = AboutPage.load()
        about_section = HomeAboutSection.objects.first() # Using first() as it's a singleton-like model
        vision_mission = VisionMission.load()
        principal = PrincipalMessage.load()
        timeline = TimelineEvent.objects.all().order_by('order', 'year')
        management = ManagementMember.objects.filter(is_active=True).order_by('order')
        facilities = Facility.objects.filter(is_active=True).order_by('order')
        
        # Get Affiliation No from General Info
        affiliation_no = ""
        try:
            affiliation_info = GeneralInfo.objects.filter(title__icontains="Affiliation").first()
            if affiliation_info:
                affiliation_no = affiliation_info.value
        except:
            pass

        data = {
            'hero_title': about_page.hero_title,
            'hero_subtitle': about_page.hero_subtitle,
            'about_section': HomeAboutPublicSerializer(about_section, context={'request': request}).data if about_section else None,
            'history_title': about_page.history_title,
            'history_content': about_page.history_content,
            'history_image': request.build_absolute_uri(about_page.history_image.url) if about_page.history_image else None,
            'infrastructure_title': about_page.infrastructure_title,
            'infrastructure_content': about_page.infrastructure_content,
            'vision_mission': VisionMissionPublicSerializer(vision_mission, context={'request': request}).data,
            'principal': PrincipalMessagePublicSerializer(principal, context={'request': request}).data,
            'timeline': TimelineEventPublicSerializer(timeline, many=True, context={'request': request}).data,
            'management': ManagementMemberPublicSerializer(management, many=True, context={'request': request}).data,
            'facilities': FacilityPublicSerializer(facilities, many=True, context={'request': request}).data,
            'affiliation_title': "Affiliations & Accreditations",
            'affiliation_content': "We are affiliated with the Central Board of Secondary Education (CBSE), New Delhi.",
            'cbse_affiliation_no': affiliation_no
        }
        return Response(data)

class ContactPagePublicView(APIView):
    """
    GET /api/public/contact/
    POST /api/public/contact/
    """
    permission_classes = [AllowAny]

    def get(self, request):
        contact_page = ContactPage.load()
        settings = SiteSettings.load()
        
        data = {
            'title': contact_page.hero_title,
            'subtitle': contact_page.hero_subtitle,
            'map_embed_code': contact_page.map_embed_code,
            'site_settings': SiteSettingsPublicSerializer(settings, context={'request': request}).data
        }
        return Response(data)

    def post(self, request):
        serializer = ContactSubmissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Thank you! Your message has been sent.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PublicDisclosureView(APIView):
    """
    GET /api/public/disclosure/
    """
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            'general_info': GeneralInfoPublicSerializer(GeneralInfo.objects.filter(is_active=True), many=True, context={'request': request}).data,
            'results': ResultsAcademicsPublicSerializer(ResultsAcademics.objects.filter(is_active=True), many=True, context={'request': request}).data,
            'infrastructure': InfrastructurePublicSerializer(Infrastructure.objects.filter(is_active=True), many=True, context={'request': request}).data,
            'fees': FeesPublicSerializer(Fees.objects.filter(is_active=True), many=True, context={'request': request}).data,
            'documents': DocumentationPublicSerializer(Documentation.objects.filter(is_active=True), many=True, context={'request': request}).data,
        })

class FacilitiesPublicView(APIView):
    """
    GET /api/public/facilities/
    """
    permission_classes = [AllowAny]

    def get(self, request):
        facilities = Facility.objects.filter(is_active=True).order_by('order')
        return Response(FacilityPublicSerializer(facilities, many=True, context={'request': request}).data)

class FacilityDetailPublicView(APIView):
    """
    GET /api/public/facilities/<slug>/
    """
    permission_classes = [AllowAny]

    def get(self, request, slug):
        facility = get_object_or_404(Facility, slug=slug, is_active=True)
        return Response(FacilityPublicSerializer(facility, context={'request': request}).data)

class PageSEOPublicView(APIView):
    """
    GET /api/public/seo/<slug>/
    """
    permission_classes = [AllowAny]

    def get(self, request, slug):
        seo = get_object_or_404(PageSEO, page_slug=slug)
        return Response(PageSEOPublicSerializer(seo, context={'request': request}).data)

# ==================== ADMIN VIEWS ====================

class SiteSettingsAdminView(APIView):
    """
    GET/PUT /api/admin/content/settings/
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        settings = SiteSettings.load()
        serializer = SiteSettingsAdminSerializer(settings, context={'request': request})
        return Response(serializer.data)

    def put(self, request):
        settings = SiteSettings.load()
        serializer = SiteSettingsAdminSerializer(settings, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        return self.put(request)

class VisionMissionAdminView(APIView):
    """
    GET/PUT /api/admin/content/vision-mission/
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        vm = VisionMission.load()
        serializer = VisionMissionPublicSerializer(vm, context={'request': request}) # Using Public serializer as fields are same for now
        return Response(serializer.data)

    def put(self, request):
        vm = VisionMission.load()
        serializer = VisionMissionPublicSerializer(vm, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        return self.put(request)

class PrincipalMessageAdminView(APIView):
    """
    GET/PUT /api/admin/content/principal/
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        pm = PrincipalMessage.load()
        serializer = PrincipalMessageAdminSerializer(pm, context={'request': request})
        return Response(serializer.data)

    def put(self, request):
        pm = PrincipalMessage.load()
        serializer = PrincipalMessageAdminSerializer(pm, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        return self.put(request)

class PrincipalMessageResetView(APIView):
    """
    POST /api/admin/content/principal/reset/
    Resets the principal section to default values.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        pm = PrincipalMessage.load()
        # Reset to defaults
        pm.name = ""
        pm.title = ""
        if pm.photo:
            pm.photo.delete(save=False)
            pm.photo = None
        pm.message = ""
        pm.qualification = ""
        pm.save()
        
        serializer = PrincipalMessageAdminSerializer(pm, context={'request': request})
        return Response({
            'message': 'Principal section reset successfully',
            'data': serializer.data
        })

from .serializers import (
    QuickLinkAdminSerializer, QuickLinkPublicSerializer,
    TestimonialAdminSerializer, TestimonialPublicSerializer,
    AchievementAdminSerializer, AchievementPublicSerializer,
    GeneralInfoAdminSerializer, GeneralInfoPublicSerializer,
    ResultsAcademicsAdminSerializer, InfrastructureAdminSerializer,
    FeesAdminSerializer, DocumentationAdminSerializer
)

class QuickLinkAdminView(APIView):
    """
    GET /api/admin/content/quick-links/
    POST /api/admin/content/quick-links/
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        links = QuickLink.objects.all()
        return Response(QuickLinkAdminSerializer(links, many=True, context={'request': request}).data)

    def post(self, request):
        serializer = QuickLinkAdminSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuickLinkDetailAdminView(APIView):
    """
    GET/PUT/DELETE /api/admin/content/quick-links/<id>/
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, pk):
        link = get_object_or_404(QuickLink, pk=pk)
        return Response(QuickLinkAdminSerializer(link, context={'request': request}).data)

    def put(self, request, pk):
        link = get_object_or_404(QuickLink, pk=pk)
        serializer = QuickLinkAdminSerializer(link, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        return self.put(request, pk)

    def delete(self, request, pk):
        link = get_object_or_404(QuickLink, pk=pk)
        link.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# --- Validating other Admin Views... Facilties, Testimonials etc. ---

class FacilityAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get(self, request):
        facilities = Facility.objects.all()
        return Response(FacilityAdminSerializer(facilities, many=True, context={'request': request}).data)
        
    def post(self, request):
        serializer = FacilityAdminSerializer(data=request.data, context={'request': request})
        # Let's use the AdminSerializer we defined
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FacilityDetailAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get(self, request, pk):
        facility = get_object_or_404(Facility, pk=pk)
        return Response(FacilityAdminSerializer(facility, context={'request': request}).data)
        
    def put(self, request, pk):
        facility = get_object_or_404(Facility, pk=pk)
        serializer = FacilityAdminSerializer(facility, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        return self.put(request, pk)
        
    def delete(self, request, pk):
        facility = get_object_or_404(Facility, pk=pk)
        facility.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TestimonialAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        items = Testimonial.objects.all()
        return Response(TestimonialAdminSerializer(items, many=True, context={'request': request}).data)

    def post(self, request):
        serializer = TestimonialAdminSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TestimonialDetailAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request, pk):
        item = get_object_or_404(Testimonial, pk=pk)
        return Response(TestimonialAdminSerializer(item, context={'request': request}).data)

    def put(self, request, pk):
        item = get_object_or_404(Testimonial, pk=pk)
        serializer = TestimonialAdminSerializer(item, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        return self.put(request, pk)

    def delete(self, request, pk):
        item = get_object_or_404(Testimonial, pk=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AchievementAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        items = Achievement.objects.all()
        return Response(AchievementAdminSerializer(items, many=True, context={'request': request}).data)

    def post(self, request):
        serializer = AchievementAdminSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AchievementDetailAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request, pk):
        item = get_object_or_404(Achievement, pk=pk)
        return Response(AchievementAdminSerializer(item, context={'request': request}).data)

    def put(self, request, pk):
        item = get_object_or_404(Achievement, pk=pk)
        serializer = AchievementAdminSerializer(item, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        return self.put(request, pk)

    def delete(self, request, pk):
        item = get_object_or_404(Achievement, pk=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# --- Disclosure Admin Views ---

class GeneralInfoAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        items = GeneralInfo.objects.all()
        return Response(GeneralInfoAdminSerializer(items, many=True, context={'request': request}).data)

    def post(self, request):
        serializer = GeneralInfoAdminSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GeneralInfoDetailAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, pk):
        item = get_object_or_404(GeneralInfo, pk=pk)
        return Response(GeneralInfoAdminSerializer(item, context={'request': request}).data)

    def put(self, request, pk):
        item = get_object_or_404(GeneralInfo, pk=pk)
        serializer = GeneralInfoAdminSerializer(item, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        return self.put(request, pk)
        
    def delete(self, request, pk):
        item = get_object_or_404(GeneralInfo, pk=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class InfrastructureAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        items = Infrastructure.objects.all()
        return Response(InfrastructureAdminSerializer(items, many=True, context={'request': request}).data)

    def post(self, request):
        serializer = InfrastructureAdminSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InfrastructureDetailAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def put(self, request, pk):
        item = get_object_or_404(Infrastructure, pk=pk)
        serializer = InfrastructureAdminSerializer(item, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        return self.put(request, pk)

    def delete(self, request, pk):
        item = get_object_or_404(Infrastructure, pk=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ResultsAdminView(APIView): # ResultsAcademics
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get(self, request):
        items = ResultsAcademics.objects.all()
        return Response(ResultsAcademicsAdminSerializer(items, many=True, context={'request': request}).data)

    def post(self, request):
        serializer = ResultsAcademicsAdminSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResultsDetailAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def put(self, request, pk):
        item = get_object_or_404(ResultsAcademics, pk=pk)
        serializer = ResultsAcademicsAdminSerializer(item, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        return self.put(request, pk)

    def delete(self, request, pk):
        item = get_object_or_404(ResultsAcademics, pk=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FeesAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        items = Fees.objects.all()
        return Response(FeesAdminSerializer(items, many=True, context={'request': request}).data)

    def post(self, request):
        serializer = FeesAdminSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FeesDetailAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def put(self, request, pk):
        item = get_object_or_404(Fees, pk=pk)
        serializer = FeesAdminSerializer(item, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        return self.put(request, pk)

    def delete(self, request, pk):
        item = get_object_or_404(Fees, pk=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DocumentationAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get(self, request):
        items = Documentation.objects.all()
        return Response(DocumentationAdminSerializer(items, many=True, context={'request': request}).data)

    def post(self, request):
        try:
            serializer = DocumentationAdminSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            print(f"Validation Errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DocumentationDetailAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def put(self, request, pk):
        item = get_object_or_404(Documentation, pk=pk)
        serializer = DocumentationAdminSerializer(item, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        return self.put(request, pk)

    def delete(self, request, pk):
        item = get_object_or_404(Documentation, pk=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# --- Missing Admin Views ---

class AboutPageAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        page = AboutPage.load()
        return Response(AboutPageAdminSerializer(page, context={'request': request}).data)

    def put(self, request):
        page = AboutPage.load()
        serializer = AboutPageAdminSerializer(page, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        return self.put(request)

# Timeline Event
class TimelineEventAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get(self, request):
        items = TimelineEvent.objects.all().order_by('year')
        return Response(TimelineEventAdminSerializer(items, many=True, context={'request': request}).data)

    def post(self, request):
        serializer = TimelineEventAdminSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TimelineEventDetailAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def put(self, request, pk):
        item = get_object_or_404(TimelineEvent, pk=pk)
        serializer = TimelineEventAdminSerializer(item, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        return self.put(request, pk)

    def delete(self, request, pk):
        item = get_object_or_404(TimelineEvent, pk=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ManagementMemberAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get(self, request):
        items = ManagementMember.objects.all().order_by('order')
        return Response(ManagementMemberAdminSerializer(items, many=True, context={'request': request}).data)

    def post(self, request):
        serializer = ManagementMemberAdminSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ManagementMemberDetailAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def put(self, request, pk):
        item = get_object_or_404(ManagementMember, pk=pk)
        serializer = ManagementMemberAdminSerializer(item, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        return self.put(request, pk)

    def delete(self, request, pk):
        item = get_object_or_404(ManagementMember, pk=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ContactPageAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        page = ContactPage.load()
        return Response(ContactPageAdminSerializer(page, context={'request': request}).data)

    def put(self, request):
        page = ContactPage.load()
        serializer = ContactPageAdminSerializer(page, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        return self.put(request)

class ContactSubmissionAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        items = ContactSubmission.objects.all().order_by('-created_at')
        return Response(ContactSubmissionAdminSerializer(items, many=True, context={'request': request}).data)

class ContactSubmissionDetailAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def put(self, request, pk):
        item = get_object_or_404(ContactSubmission, pk=pk)
        serializer = ContactSubmissionAdminSerializer(item, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        return self.put(request, pk)

    def delete(self, request, pk):
        item = get_object_or_404(ContactSubmission, pk=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FacilityGalleryAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get(self, request, pk):
        facility = get_object_or_404(Facility, pk=pk)
        images = FacilityImage.objects.filter(facility=facility).order_by('order')
        return Response(FacilityImageReadSerializer(images, many=True, context={'request': request}).data)

    def post(self, request, pk):
        import json
        facility = get_object_or_404(Facility, pk=pk)
        
        # Debug logging to file
        with open('debug_log.txt', 'a') as f:
            f.write(f"\n--- REQUEST DATA ---\n{request.data}\n")

        # Use CreateSerializer which excludes 'facility' field
        serializer = FacilityImageCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(facility=facility)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        with open('debug_log.txt', 'a') as f:
            f.write(f"--- ERRORS ---\n{serializer.errors}\n")
            
        print(f"Facility Image Upload Error: {serializer.errors}") 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FacilityImageDetailAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def put(self, request, pk):
        image = get_object_or_404(FacilityImage, pk=pk)
        serializer = FacilityImageAdminSerializer(image, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        return self.put(request, pk)

    def delete(self, request, pk):
        image = get_object_or_404(FacilityImage, pk=pk)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PageSEOAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get(self, request):
        items = PageSEO.objects.all()
        return Response(PageSEOAdminSerializer(items, many=True, context={'request': request}).data)

    def post(self, request):
        serializer = PageSEOAdminSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PageSEODetailAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def put(self, request, pk):
        item = get_object_or_404(PageSEO, pk=pk)
        serializer = PageSEOAdminSerializer(item, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        return self.put(request, pk)

    def delete(self, request, pk):
        item = get_object_or_404(PageSEO, pk=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
