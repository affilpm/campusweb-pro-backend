"""
Content app serializers.
Consolidated serializers from separate feature apps.
"""

from rest_framework import serializers
from .models import (
    SiteSettings, HeroSection, VisionMission, HomeAboutSection, PrincipalMessage, QuickLink,
    Notice, Event, GalleryCategory, GalleryImage, Facility, FacilityImage,
    Achievement, Testimonial, Download, Documentation,
    AcademicHighlight, ClassCategory, Subject, AcademicsPage,
    AdmissionSettings, AdmissionStep,
    AboutPage, TimelineEvent, ManagementMember,
    GeneralInfo, ResultsAcademics, Infrastructure, Fees,
    PageSEO, ContactPage, ContactSubmission
)


# --- Schools / Site Settings ---

class SiteSettingsAdminSerializer(serializers.ModelSerializer):
    address = serializers.CharField(source='school_address', required=False, allow_blank=True)
    phone = serializers.CharField(source='school_phone', required=False, allow_blank=True)
    email = serializers.EmailField(source='school_email', required=False, allow_blank=True)

    class Meta:
        model = SiteSettings
        fields = [
            'id', 'school_name', 'school_motto', 'school_logo', 'favicon',
            'address', 'phone', 'email',  # Use mapped field names
            'facebook_url', 'instagram_url', 'twitter_url', 'youtube_url', 'linkedin_url',
            'google_maps_link',
            'footer_text'
        ]


class SiteSettingsPublicSerializer(serializers.ModelSerializer):
    school_logo = serializers.SerializerMethodField()
    favicon = serializers.SerializerMethodField()
    # Map model fields to frontend expected field names
    address = serializers.CharField(source='school_address', read_only=True)
    phone = serializers.CharField(source='school_phone', read_only=True)
    email = serializers.EmailField(source='school_email', read_only=True)
    school_motto = serializers.SerializerMethodField()
    footer_text = serializers.SerializerMethodField()

    class Meta:
        model = SiteSettings
        fields = [
            'id', 'school_name', 'school_motto', 'school_logo', 'favicon',
            'address', 'phone', 'email',
            'facebook_url', 'instagram_url', 'twitter_url', 'youtube_url', 'linkedin_url',
            'google_maps_link',
            'footer_text'
        ]

    def get_school_logo(self, obj):
        if obj.school_logo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.school_logo.url)
            return obj.school_logo.url
        return None

    def get_favicon(self, obj):
        if obj.favicon:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.favicon.url)
            return obj.favicon.url
        return None

    def get_school_motto(self, obj):
        # Return a default motto if not available in model
        return "Empowering Minds, Shaping Futures"

    def get_footer_text(self, obj):
        # Return empty string (frontend has fallback)
        return ""


class HeroSectionPublicSerializer(serializers.ModelSerializer):
    background_image = serializers.SerializerMethodField()

    class Meta:
        model = HeroSection
        fields = ['id', 'title', 'subtitle', 'background_image', 'cta_text', 'cta_link']

    def get_background_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class VisionMissionPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisionMission
        exclude = ['created_at', 'updated_at']


class HomeAboutSectionPublicSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = HomeAboutSection
        exclude = ['created_at', 'updated_at']
    
    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class PrincipalMessagePublicSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = PrincipalMessage
        exclude = ['created_at', 'updated_at']

    def get_photo(self, obj):
        if obj.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo.url)
            return obj.photo.url
        return None


class QuickLinkPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuickLink
        fields = ['id', 'title', 'url', 'open_in_new_tab']


class HomepageDataSerializer(serializers.Serializer):
    """
    Aggregated data for homepage.
    """
    hero = HeroSectionPublicSerializer()
    about = HomeAboutSectionPublicSerializer()
    vision_mission = VisionMissionPublicSerializer()
    principal_message = PrincipalMessagePublicSerializer()
    academics = serializers.ListField()  # AcademicHighlight
    notices = serializers.ListField()    # Notice
    events = serializers.ListField()     # Event
    testimonials = serializers.ListField() # Testimonial
    stats = serializers.DictField()      # Dynamic stats if any


# Admin Serializers
class HeroSectionAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroSection
        fields = '__all__'


class VisionMissionAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisionMission
        fields = '__all__'


class HomeAboutSectionAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeAboutSection
        fields = '__all__'


class PrincipalMessageAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrincipalMessage
        fields = '__all__'


class QuickLinkAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuickLink
        fields = '__all__'


# --- Notices ---

class NoticePublicSerializer(serializers.ModelSerializer):
    attachment = serializers.SerializerMethodField()

    class Meta:
        model = Notice
        fields = [
            'id', 'title', 'content', 'attachment',
            'is_important', 'publish_date'
        ]

    def get_attachment(self, obj):
        if obj.attachment:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.attachment.url)
            return obj.attachment.url
        return None


class NoticeAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


# --- Events ---

class EventPublicSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'slug', 'excerpt', 'content',
            'image', 'event_date', 'is_featured', 'created_at'
        ]

    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class EventListPublicSerializer(serializers.ModelSerializer):
    """Lighter serializer for list views."""
    image = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'slug', 'excerpt',
            'image', 'event_date', 'is_featured'
        ]

    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class EventAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


# --- Gallery ---

class GalleryCategoryPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryCategory
        fields = ['id', 'name', 'slug']


class GalleryImagePublicSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = GalleryImage
        fields = ['id', 'title', 'image', 'category', 'category_name', 'caption', 'is_featured']

    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class GalleryCategoryAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryCategory
        fields = '__all__'


class GalleryImageAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryImage
        fields = '__all__'
        read_only_fields = ['created_at']


# --- Facilities ---

class FacilityImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = FacilityImage
        fields = ['id', 'image', 'caption', 'order']

    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class FacilityPublicSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    description = serializers.CharField(source='short_description')

    class Meta:
        model = Facility
        fields = ['id', 'name', 'slug', 'description', 'icon', 'image']

    def get_image(self, obj):
        if obj.cover_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.cover_image.url)
            return obj.cover_image.url
        return None


class FacilityDetailSerializer(serializers.ModelSerializer):
    cover_image = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    gallery = serializers.SerializerMethodField()

    class Meta:
        model = Facility
        fields = ['id', 'name', 'slug', 'short_description', 'long_description', 'icon', 'cover_image', 'image', 'gallery']

    def get_cover_image(self, obj):
        if obj.cover_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.cover_image.url)
            return obj.cover_image.url
        return None

    def get_image(self, obj):
        return self.get_cover_image(obj)

    def get_gallery(self, obj):
        images = obj.gallery_images.filter(is_active=True).order_by('order')
        return FacilityImageSerializer(images, many=True, context=self.context).data


class FacilityImageAdminSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FacilityImage
        fields = ['id', 'facility', 'image', 'image_url', 'caption', 'order', 'is_active']
        read_only_fields = ['facility']
        extra_kwargs = {
            'image': {'write_only': True, 'required': False}
        }

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self.get_image_url(instance)
        return representation


class FacilityAdminSerializer(serializers.ModelSerializer):
    cover_image_url = serializers.SerializerMethodField(read_only=True)
    gallery_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Facility
        fields = ['id', 'name', 'slug', 'short_description', 'long_description', 'icon', 
                  'cover_image', 'cover_image_url', 'order', 'is_active', 'gallery_count']
        extra_kwargs = {
            'cover_image': {'write_only': True, 'required': False}
        }

    def get_cover_image_url(self, obj):
        if obj.cover_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.cover_image.url)
            return obj.cover_image.url
        return None

    def get_gallery_count(self, obj):
        return obj.gallery_images.count()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self.get_cover_image_url(instance)
        return representation


# --- Achievements ---

class AchievementPublicSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Achievement
        fields = ['id', 'title', 'description', 'image', 'year']

    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class AchievementAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = '__all__'


# --- Testimonials ---

class TestimonialPublicSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = Testimonial
        fields = ['id', 'name', 'role', 'content', 'rating', 'photo']

    def get_photo(self, obj):
        if obj.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo.url)
            return obj.photo.url
        return None


class TestimonialAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'


# --- Downloads ---

class DownloadPublicSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = Download
        fields = ['id', 'title', 'description', 'category', 'file', 'download_count', 'created_at']

    def get_file(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None


class DocumentationPublicSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = Documentation
        fields = ['id', 'title', 'description', 'file']

    def get_file(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None


class DownloadAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Download
        fields = '__all__'
        read_only_fields = ['download_count', 'created_at']


class DocumentationAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documentation
        fields = '__all__'


# --- Academics ---

class AcademicHighlightPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicHighlight
        fields = ['id', 'title', 'value', 'icon']


class SubjectPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'description', 'is_core']


class ClassCategoryPublicSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    subjects = serializers.SerializerMethodField()

    class Meta:
        model = ClassCategory
        fields = ['id', 'name', 'description', 'image', 'subjects']

    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

    def get_subjects(self, obj):
        return SubjectPublicSerializer(obj.subjects.all().order_by('order'), many=True).data


class AcademicsPagePublicSerializer(serializers.ModelSerializer):
    hero_image = serializers.SerializerMethodField()
    curriculum_image = serializers.SerializerMethodField()
    calendar_file = serializers.SerializerMethodField()
    class_categories = serializers.SerializerMethodField()

    class Meta:
        model = AcademicsPage
        fields = [
            'hero_title', 'hero_subtitle', 'hero_image',
            'overview_title', 'overview_content',
            'curriculum_title', 'curriculum_content', 'curriculum_image',
            'methodology_title', 'methodology_content',
            'calendar_title', 'calendar_file',
            'class_categories'
        ]

    def get_hero_image(self, obj):
        if obj.hero_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.hero_image.url)
            return obj.hero_image.url
        return None

    def get_curriculum_image(self, obj):
        if obj.curriculum_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.curriculum_image.url)
            return obj.curriculum_image.url
        return None

    def get_calendar_file(self, obj):
        if obj.calendar_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.calendar_file.url)
            return obj.calendar_file.url
        return None

    def get_class_categories(self, obj):
        categories = ClassCategory.objects.all().order_by('order')
        return ClassCategoryPublicSerializer(categories, many=True, context=self.context).data


# Admin serializers
class AcademicHighlightAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicHighlight
        fields = '__all__'


class ClassCategoryAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassCategory
        fields = '__all__'


class SubjectAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class AcademicsPageAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicsPage
        fields = '__all__'


# --- Admissions ---

class AdmissionStepPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdmissionStep
        fields = ['id', 'title', 'description', 'icon', 'order']


class AdmissionSettingsPublicSerializer(serializers.ModelSerializer):
    hero_image = serializers.SerializerMethodField()
    steps = serializers.SerializerMethodField()

    class Meta:
        model = AdmissionSettings
        fields = [
            'is_open', 'hero_title', 'hero_subtitle', 'hero_image',
            'overview_title', 'overview_content',
            'eligibility_title', 'eligibility_content',
            'documents_required', 'contact_info', 'application_form_link',
            'steps'
        ]

    def get_hero_image(self, obj):
        if obj.hero_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.hero_image.url)
            return obj.hero_image.url
        return None

    def get_steps(self, obj):
        steps = AdmissionStep.objects.all().order_by('order')
        return AdmissionStepPublicSerializer(steps, many=True).data


class AdmissionSettingsAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdmissionSettings
        fields = '__all__'


class AdmissionStepAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdmissionStep
        fields = '__all__'


# --- About Page ---

class TimelineEventPublicSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = TimelineEvent
        fields = ['id', 'year', 'title', 'description', 'image']

    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class ManagementMemberPublicSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = ManagementMember
        fields = ['id', 'name', 'position', 'photo', 'bio']

    def get_photo(self, obj):
        if obj.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo.url)
            return obj.photo.url
        return None


class AboutPagePublicSerializer(serializers.ModelSerializer):
    history_image = serializers.SerializerMethodField()
    timeline = serializers.SerializerMethodField()
    management = serializers.SerializerMethodField()

    class Meta:
        model = AboutPage
        fields = [
            'hero_title', 'hero_subtitle',
            'history_title', 'history_content', 'history_image',
            'infrastructure_title', 'infrastructure_content',
            'timeline', 'management'
        ]


    def get_history_image(self, obj):
        if obj.history_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.history_image.url)
            return obj.history_image.url
        return None

    def get_timeline(self, obj):
        events = TimelineEvent.objects.all().order_by('order')
        return TimelineEventPublicSerializer(events, many=True, context=self.context).data

    def get_management(self, obj):
        members = ManagementMember.objects.filter(is_active=True).order_by('order')
        return ManagementMemberPublicSerializer(members, many=True, context=self.context).data


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
        fields = ['id', 'title', 'value']


class ResultsAcademicsPublicSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = ResultsAcademics
        fields = ['id', 'title', 'value', 'file']

    def get_file(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None


class InfrastructurePublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Infrastructure
        fields = ['id', 'title', 'value']


class FeesPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fees
        fields = ['id', 'title', 'value']


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


# --- SEO ---

class PageSEOPublicSerializer(serializers.ModelSerializer):
    og_image = serializers.SerializerMethodField()

    class Meta:
        model = PageSEO
        fields = ['page_slug', 'title', 'meta_description', 'meta_keywords', 'og_image']

    def get_og_image(self, obj):
        if obj.og_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.og_image.url)
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
    address = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = ContactPage
        fields = [
            'hero_title', 'hero_subtitle',
            'address', 'phone', 'email',
            'map_embed_code', 'office_hours', 'school_hours'
        ]

    def get_address(self, obj):
        # Source from SiteSettings if available, else fallback to model
        settings = SiteSettings.load()
        return settings.school_address or obj.address

    def get_phone(self, obj):
        settings = SiteSettings.load()
        return settings.school_phone or obj.phone

    def get_email(self, obj):
        settings = SiteSettings.load()
        return settings.school_email or obj.email


class ContactSubmissionSerializer(serializers.ModelSerializer):
    """For public form submission."""
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
        read_only_fields = ['created_at']
