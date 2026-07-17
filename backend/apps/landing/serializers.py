from rest_framework import serializers
from apps.core.serializers import URLSafeImageMixin

from .models import HeroSection, HomeAboutSection, AcademicHighlight
from apps.school_info.serializers import (
    SiteSettingsPublicSerializer, AboutPagePublicSerializer, 
    PrincipalMessagePublicSerializer, FacilityPublicSerializer,
    GeneralInfoPublicSerializer,
    TestimonialPublicSerializer, AchievementPublicSerializer
)
from apps.communication.serializers import NoticePublicSerializer, EventPublicSerializer
from apps.academics.serializers import AcademicsPagePublicSerializer
from apps.gallery.serializers import GalleryImagePublicSerializer
from apps.admissions.serializers import AdmissionSettingsPublicSerializer

class HeroSectionPublicSerializer(serializers.ModelSerializer):
    background_image = serializers.SerializerMethodField()
    
    class Meta:
        model = HeroSection
        fields = ['title', 'subtitle', 'background_image']
        
    def get_background_image(self, obj):
        if obj.image:
             return obj.image.url
        return None

class HomeAboutPublicSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = HomeAboutSection
        exclude = ['created_at', 'updated_at']
        
    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None

class HomeAboutAdminSerializer(URLSafeImageMixin, serializers.ModelSerializer):
    class Meta:
        model = HomeAboutSection
        fields = '__all__'

class AcademicHighlightAdminSerializer(URLSafeImageMixin, serializers.ModelSerializer):
    class Meta:
        model = AcademicHighlight
        fields = '__all__'

class HeroSectionAdminSerializer(URLSafeImageMixin, serializers.ModelSerializer):
    class Meta:
        model = HeroSection
        fields = '__all__'
