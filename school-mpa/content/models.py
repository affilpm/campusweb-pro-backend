"""
Content app models.
All content models for the school website.
"""

from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from core.models import TenantAwareModel, SingletonTenantModel
from core.utils import (
    unique_upload_path, logos_upload_path, hero_upload_path,
    about_upload_path, principal_upload_path,
    notices_upload_path, events_upload_path,
    gallery_upload_path,
    facilities_upload_path, facilities_gallery_upload_path,
    achievements_upload_path, testimonials_upload_path,
    documentation_upload_path,
    academics_upload_path, admissions_upload_path,
    about_timeline_upload_path, about_management_upload_path,
    results_upload_path, seo_upload_path
)


# --- Site Settings ---

class SiteSettings(SingletonTenantModel):
    """Global site settings."""
    school_name = models.CharField(max_length=255, default="My School")
    school_address = models.TextField(blank=True, default="")
    school_email = models.EmailField(blank=True, default="")
    school_phone = models.TextField(blank=True, default="", help_text="Multiple phones separated by commas")
    school_logo = models.ImageField(upload_to=logos_upload_path, blank=True, null=True)
    favicon = models.ImageField(upload_to=logos_upload_path, blank=True, null=True)
    school_motto = models.CharField(max_length=500, blank=True, default="")
    footer_text = models.TextField(blank=True, default="")
    
    # Social Media
    facebook_url = models.URLField(blank=True, default="")
    instagram_url = models.URLField(blank=True, default="")
    twitter_url = models.URLField(blank=True, default="")
    youtube_url = models.URLField(blank=True, default="")
    linkedin_url = models.URLField(blank=True, default="")
    google_maps_link = models.URLField(blank=True, default="")

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Settings"
    
    def get_phones(self):
        """Return list of phone numbers."""
        if not self.school_phone:
            return []
        return [p.strip() for p in self.school_phone.replace('\n', ',').split(',') if p.strip()]


class HeroSection(SingletonTenantModel):
    """Homepage hero section."""
    title = models.CharField(max_length=255, default="Welcome to Our School")
    subtitle = models.TextField(blank=True, default="Empowering Minds, Shaping Futures")
    image = models.ImageField(upload_to=hero_upload_path, blank=True, null=True)
    cta_text = models.CharField(max_length=50, default="Admissions Open")
    cta_link = models.CharField(max_length=255, default="/admissions")

    class Meta:
        verbose_name = "Hero Section"

    def __str__(self):
        return "Hero Section"


class VisionMission(SingletonTenantModel):
    """Vision and Mission."""
    vision_title = models.CharField(max_length=255, default="Our Vision")
    vision_content = models.TextField(blank=True, default="")
    mission_title = models.CharField(max_length=255, default="Our Mission")
    mission_content = models.TextField(blank=True, default="")
    values_title = models.CharField(max_length=255, default="Core Values")
    values_content = models.TextField(blank=True, default="")

    class Meta:
        verbose_name = "Vision & Mission"

    def __str__(self):
        return "Vision & Mission"


class HomeAboutSection(SingletonTenantModel):
    """Homepage about section."""
    title = models.CharField(max_length=255, default="About Us")
    content = models.TextField(blank=True, default="")
    image = models.ImageField(upload_to=about_upload_path, blank=True, null=True)
    established_year = models.PositiveIntegerField(default=2000)
    students_count = models.CharField(max_length=50, default="500+")
    teachers_count = models.CharField(max_length=50, default="30+")

    class Meta:
        verbose_name = "About Section (Home)"

    def __str__(self):
        return "About Section (Home)"


class PrincipalMessage(SingletonTenantModel):
    """Principal/Director message."""
    name = models.CharField(max_length=255, default="Principal Name")
    title = models.CharField(max_length=100, default="Principal")
    photo = models.ImageField(upload_to=principal_upload_path, blank=True, null=True)
    message = models.TextField(blank=True, default="")
    qualification = models.CharField(max_length=255, blank=True, default="")

    class Meta:
        verbose_name = "Principal Message"

    def __str__(self):
        return f"Message from {self.name}"


class QuickLink(models.Model):
    """Quick links for footer/sidebar."""
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    open_in_new_tab = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


# --- Notices ---

class Notice(TenantAwareModel):
    """School notices and announcements."""
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'
        ARCHIVED = 'archived', 'Archived'

    title = models.CharField(max_length=255)
    content = models.TextField()
    attachment = models.FileField(upload_to=notices_upload_path, blank=True, null=True)
    is_important = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    publish_date = models.DateField(default=timezone.now)
    expiry_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['-is_important', '-publish_date', '-created_at']

    def __str__(self):
        return self.title


# --- Events ---

class Event(TenantAwareModel):
    """School events and news."""
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'
        ARCHIVED = 'archived', 'Archived'

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    excerpt = models.TextField(max_length=500, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to=events_upload_path, blank=True, null=True)
    event_date = models.DateField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)

    class Meta:
        ordering = ['-is_featured', '-event_date', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Event.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# --- Gallery ---

class GalleryCategory(TenantAwareModel):
    """Gallery categories."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Gallery Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class GalleryImage(TenantAwareModel):
    """Gallery images."""
    category = models.ForeignKey(GalleryCategory, on_delete=models.CASCADE, related_name='images')
    title = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to=gallery_upload_path)
    caption = models.CharField(max_length=255, blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-is_featured', 'order', '-created_at']

    def __str__(self):
        return self.title or f"Gallery Image {self.pk}"


# --- Facilities ---

class Facility(TenantAwareModel):
    """School facilities."""
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)
    short_description = models.TextField(default="")
    long_description = models.TextField(blank=True, default="")
    icon = models.CharField(max_length=50, default="🏫")
    cover_image = models.ImageField(upload_to=facilities_upload_path, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Facilities"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Facility.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class FacilityImage(TenantAwareModel):
    """Gallery images for a facility."""
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to=facilities_gallery_upload_path)
    caption = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.facility.name} - Image {self.order}"


# --- Achievements ---

class Achievement(TenantAwareModel):
    """School achievements and recognitions."""
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to=achievements_upload_path, blank=True, null=True)
    year = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title


# --- Testimonials ---

class Testimonial(TenantAwareModel):
    """Student/Parent testimonials."""
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=100, help_text="e.g., Parent, Alumni, Student")
    photo = models.ImageField(upload_to=testimonials_upload_path, blank=True, null=True)
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.name} - {self.role}"


# --- Documentation ---

class Documentation(TenantAwareModel):
    """Documentation/certificates to display."""
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to=documentation_upload_path, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title


# --- Academics ---

class AcademicHighlight(TenantAwareModel):
    """Academic highlights for homepage."""
    title = models.CharField(max_length=100)
    value = models.CharField(max_length=50)
    icon = models.CharField(max_length=50, default="📚")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class ClassCategory(TenantAwareModel):
    """Class categories (e.g., Primary, Secondary)."""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    classes_range = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to=academics_upload_path, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Class Categories"

    def __str__(self):
        return self.name


class Subject(TenantAwareModel):
    """Subjects offered."""
    categories = models.ManyToManyField(ClassCategory, related_name='subjects')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    is_core = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class AcademicsPage(SingletonTenantModel):
    """Academics page settings."""
    hero_title = models.CharField(max_length=255, default="Academics")
    hero_subtitle = models.TextField(blank=True)
    hero_image = models.ImageField(upload_to=academics_upload_path, blank=True, null=True)
    overview_title = models.CharField(max_length=255, default="Academic Excellence")
    overview_content = models.TextField(blank=True)
    curriculum_title = models.CharField(max_length=255, default="Our Curriculum")
    curriculum_content = models.TextField(blank=True)
    curriculum_image = models.ImageField(upload_to=academics_upload_path, blank=True, null=True)
    methodology_title = models.CharField(max_length=255, default="Our Teaching Methodology")
    methodology_content = models.TextField(blank=True)
    calendar_title = models.CharField(max_length=255, default="Academic Calendar")
    calendar_file = models.FileField(upload_to=academics_upload_path, blank=True, null=True)

    class Meta:
        verbose_name = "Academics Page"

    def __str__(self):
        return "Academics Page"


# --- Admissions ---

class AdmissionSettings(SingletonTenantModel):
    """Admission settings."""
    is_open = models.BooleanField(default=True)
    hero_title = models.CharField(max_length=255, default="Admissions")
    hero_subtitle = models.TextField(blank=True)
    hero_image = models.ImageField(upload_to=admissions_upload_path, blank=True, null=True)
    overview_title = models.CharField(max_length=255, default="Admission Process")
    overview_content = models.TextField(blank=True)
    eligibility_title = models.CharField(max_length=255, default="Eligibility Criteria")
    eligibility_content = models.TextField(blank=True)
    documents_required = models.TextField(blank=True, help_text="One document per line")
    contact_info = models.TextField(blank=True)
    application_form_link = models.URLField(blank=True)

    class Meta:
        verbose_name = "Admission Settings"

    def __str__(self):
        return "Admission Settings"
    
    def get_documents_list(self):
        """Return documents as a list."""
        if not self.documents_required:
            return []
        return [d.strip() for d in self.documents_required.split('\n') if d.strip()]


class AdmissionStep(TenantAwareModel):
    """Steps in admission process."""
    title = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.CharField(max_length=50, default="📝")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Step {self.order}: {self.title}"


# --- About Page ---

class AboutPage(SingletonTenantModel):
    """About page settings."""
    hero_title = models.CharField(max_length=255, default="About Our School")
    hero_subtitle = models.TextField(blank=True)
    history_title = models.CharField(max_length=255, default="Our History")
    history_content = models.TextField(blank=True)
    history_image = models.ImageField(upload_to=about_upload_path, blank=True, null=True)
    infrastructure_title = models.CharField(max_length=255, default="Our Infrastructure", blank=True)
    infrastructure_content = models.TextField(blank=True)

    class Meta:
        verbose_name = "About Page"

    def __str__(self):
        return "About Page"


class TimelineEvent(TenantAwareModel):
    """Timeline events for school history."""
    year = models.CharField(max_length=20)
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to=about_timeline_upload_path, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'year']

    def __str__(self):
        return f"{self.year} - {self.title}"


class ManagementMember(TenantAwareModel):
    """Management/Staff members."""
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    photo = models.ImageField(upload_to=about_management_upload_path, blank=True, null=True)
    bio = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name} - {self.position}"


# --- Public Disclosure ---

class GeneralInfo(TenantAwareModel):
    """General information items for public disclosure."""
    title = models.CharField(max_length=255)
    value = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name_plural = "General Info"

    def __str__(self):
        return self.title


class ResultsAcademics(TenantAwareModel):
    """Results and academics for public disclosure."""
    title = models.CharField(max_length=255)
    value = models.TextField(blank=True)
    file = models.FileField(upload_to=results_upload_path, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name_plural = "Results & Academics"

    def __str__(self):
        return self.title


class Infrastructure(TenantAwareModel):
    """Infrastructure details for public disclosure."""
    title = models.CharField(max_length=255)
    value = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


class Fees(TenantAwareModel):
    """Fee structure for public disclosure."""
    title = models.CharField(max_length=255)
    value = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name_plural = "Fees"

    def __str__(self):
        return self.title


# --- SEO ---

class PageSEO(TenantAwareModel):
    """SEO settings for individual pages."""
    page_slug = models.CharField(max_length=100, unique=True, help_text="e.g., home, about, contact")
    title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True, max_length=500)
    meta_keywords = models.CharField(max_length=500, blank=True)
    og_image = models.ImageField(upload_to=seo_upload_path, blank=True, null=True)

    class Meta:
        verbose_name = "Page SEO"
        verbose_name_plural = "Page SEO"

    def __str__(self):
        return f"SEO: {self.page_slug}"


# --- Contact ---

class ContactPage(SingletonTenantModel):
    """Contact page settings."""
    hero_title = models.CharField(max_length=255, default="Contact Us")
    hero_subtitle = models.TextField(blank=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    map_embed_code = models.TextField(blank=True, help_text="Google Maps embed iframe code")
    office_hours = models.TextField(blank=True)
    school_hours = models.TextField(blank=True)

    class Meta:
        verbose_name = "Contact Page"

    def __str__(self):
        return "Contact Page"


class ContactSubmission(TenantAwareModel):
    """Contact form submissions."""
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    is_replied = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"
