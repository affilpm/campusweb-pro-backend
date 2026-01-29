from rest_framework import serializers
from .models import (
    SiteSettings, VisionMission, PrincipalMessage, QuickLink,
    AboutPage, TimelineEvent, ManagementMember,
    GeneralInfo, ResultsAcademics, Infrastructure, Fees,
    Documentation, PageSEO, ContactPage, ContactSubmission,
    Testimonial, Achievement, Facility, FacilityImage
)

# --- Site Settings ---

class SiteSettingsAdminSerializer(serializers.ModelSerializer):
    address = serializers.CharField(source='school_address', required=False, allow_blank=True)
    phone = serializers.CharField(source='school_phone', required=False, allow_blank=True)
    email = serializers.EmailField(source='school_email', required=False, allow_blank=True)

    class Meta:
        model = SiteSettings
        fields = [
            'id', 'school_name', 'school_motto', 'school_description', 'school_logo', 'favicon',
            'address', 'phone', 'email',  # Use mapped field names
            'facebook_url', 'instagram_url', 'twitter_url', 'youtube_url', 'linkedin_url',
            'google_maps_link',
            'footer_text',
            'school_hours', 'office_hours'
        ]

class SiteSettingsPublicSerializer(serializers.ModelSerializer):
    school_logo = serializers.SerializerMethodField()
    favicon = serializers.SerializerMethodField()
    address = serializers.CharField(source='school_address', read_only=True)
    phone = serializers.CharField(source='school_phone', read_only=True)
    email = serializers.EmailField(source='school_email', read_only=True)
    
    # Computed fields to ensure they return strings not null
    school_motto = serializers.SerializerMethodField()
    footer_text = serializers.SerializerMethodField()
    school_hours = serializers.SerializerMethodField()
    office_hours = serializers.SerializerMethodField()

    class Meta:
        model = SiteSettings
        fields = [
            'id', 'school_name', 'school_motto', 'school_description', 'school_logo', 'favicon',
            'address', 'phone', 'email',
            'facebook_url', 'instagram_url', 'twitter_url', 'youtube_url', 'linkedin_url',
            'google_maps_link',
            'footer_text',
            'school_hours', 'office_hours'
        ]

    def get_school_logo(self, obj):
        if obj.school_logo:
             return obj.school_logo.url
        return None

    def get_favicon(self, obj):
        if obj.favicon:
             return obj.favicon.url
        return None
        
    def get_school_motto(self, obj):
        return obj.school_motto or ""

    def get_footer_text(self, obj):
        return obj.footer_text or ""

    def get_school_hours(self, obj):
        return obj.school_hours or ""

    def get_office_hours(self, obj):
        return obj.office_hours or ""

# --- Vision Mission ---

class VisionMissionPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisionMission
        exclude = ['created_at', 'updated_at']

# --- Principal Message ---

class PrincipalMessagePublicSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = PrincipalMessage
        exclude = ['created_at', 'updated_at']

    def get_photo(self, obj):
        if obj.photo:
            return obj.photo.url
        return None

class PrincipalMessageAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrincipalMessage
        fields = '__all__'

# --- Quick Links ---

class QuickLinkPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuickLink
        fields = ['id', 'title', 'url', 'open_in_new_tab']

# --- About Page ---

class AboutPagePublicSerializer(serializers.ModelSerializer):
    history_image = serializers.SerializerMethodField()
    
    class Meta:
        model = AboutPage
        exclude = ['created_at', 'updated_at']
        
    def get_history_image(self, obj):
        if obj.history_image:
            return obj.history_image.url
        return None

class TimelineEventPublicSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = TimelineEvent
        exclude = ['created_at', 'updated_at']
        
    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None

class ManagementMemberPublicSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    
    class Meta:
        model = ManagementMember
        exclude = ['created_at', 'updated_at']
        
    def get_photo(self, obj):
        if obj.photo:
            return obj.photo.url
        return None

# Admin Serializers for About Page
class AboutPageAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutPage
        fields = '__all__'

class TimelineEventAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimelineEvent
        fields = '__all__'

class ManagementMemberAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagementMember
        fields = '__all__'

# --- Public Disclosure ---

class GeneralInfoPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralInfo
        fields = ['id', 'title', 'value', 'order']

class ResultsAcademicsPublicSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()
    
    class Meta:
        model = ResultsAcademics
        fields = ['id', 'title', 'value', 'file', 'order']
        
    def get_file(self, obj):
        if obj.file:
            return obj.file.url
        return None

class InfrastructurePublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Infrastructure
        fields = ['id', 'title', 'value', 'order']

class FeesPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fees
        fields = ['id', 'title', 'value', 'order']

class DocumentationPublicSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()
    
    class Meta:
        model = Documentation
        fields = ['id', 'title', 'description', 'file', 'order', 'created_at']
        
    def get_file(self, obj):
        if obj.file:
            return obj.file.url
        return None

# --- Facilities ---

class FacilityImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = FacilityImage
        fields = ['id', 'image', 'caption', 'order']
        
    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None

class FacilityPublicSerializer(serializers.ModelSerializer):
    cover_image = serializers.SerializerMethodField()
    gallery_images = serializers.SerializerMethodField()
    
    class Meta:
        model = Facility
        fields = ['id', 'name', 'slug', 'short_description', 'long_description', 'icon', 'cover_image', 'gallery_images']
        
    def get_cover_image(self, obj):
        if obj.cover_image:
            return obj.cover_image.url
        return None

    def get_gallery_images(self, obj):
        # Only show active images in correct order
        images = obj.gallery_images.filter(is_active=True).order_by('order')
        return FacilityImageSerializer(images, many=True, context=self.context).data

# --- Achievements ---

class AchievementPublicSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Achievement
        fields = ['id', 'title', 'description', 'image', 'year']
        
    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None

# --- Testimonials ---

class TestimonialPublicSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    
    class Meta:
        model = Testimonial
        fields = ['id', 'name', 'role', 'photo', 'content', 'rating']
        
    def get_photo(self, obj):
        if obj.photo:
            return obj.photo.url
        return None

# --- SEO ---

class PageSEOPublicSerializer(serializers.ModelSerializer):
    og_image = serializers.SerializerMethodField()
    
    class Meta:
        model = PageSEO
        fields = ['page_slug', 'title', 'meta_description', 'meta_keywords', 'og_image']
        
    def get_og_image(self, obj):
        if obj.og_image:
            return obj.og_image.url
        return None

class PageSEOAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageSEO
        fields = '__all__'

# --- Contact ---

class ContactPagePublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactPage
        exclude = ['created_at', 'updated_at']

class ContactSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'phone', 'subject', 'message']

class ContactPageAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactPage
        fields = '__all__'

class ContactSubmissionAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSubmission
        fields = '__all__'

# --- Quick Links ---
class QuickLinkAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuickLink
        fields = '__all__'

# --- Testimonials ---
class TestimonialAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'

# --- Achievements ---
class AchievementAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = '__all__'

# --- Facilities ---
class FacilityImageReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacilityImage
        fields = '__all__'

class FacilityImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacilityImage
        exclude = ['facility']

class FacilityImageAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacilityImage
        exclude = ['facility']

class FacilityAdminSerializer(serializers.ModelSerializer):
    gallery_images = FacilityImageAdminSerializer(many=True, read_only=True)
    image = serializers.ImageField(source='cover_image', read_only=True)

    class Meta:
        model = Facility
        fields = '__all__'

# --- Public Disclosure ---
class GeneralInfoAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralInfo
        fields = '__all__'

class ResultsAcademicsAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultsAcademics
        fields = '__all__'

class InfrastructureAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Infrastructure
        fields = '__all__'

class FeesAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fees
        fields = '__all__'

class DocumentationAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documentation
        fields = '__all__'
