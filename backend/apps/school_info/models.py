from django.db import models
from apps.core.models import TenantAwareModel, SingletonTenantModel
from apps.core.utils import (
    logos_upload_path, principal_upload_path, facilities_upload_path,
    facilities_gallery_upload_path, achievements_upload_path,
    testimonials_upload_path, about_timeline_upload_path,
    about_management_upload_path, results_upload_path,
    documentation_upload_path, seo_upload_path, about_upload_path, compress_image
)
from django.utils.text import slugify

class SiteSettings(SingletonTenantModel):
    """
    Global site settings.
    """
    school_name = models.CharField(max_length=255, default="My School")
    school_address = models.TextField(blank=True, default="")
    school_email = models.EmailField(blank=True, default="")
    school_phone = models.TextField(blank=True, default="", help_text="Enter multiple phone numbers separated by commas or newlines")
    school_logo = models.ImageField(upload_to=logos_upload_path, blank=True, null=True)
    favicon = models.ImageField(upload_to=logos_upload_path, blank=True, null=True)
    
    school_motto = models.CharField(max_length=500, blank=True, default="")
    school_description = models.TextField(blank=True, default="Committed to providing quality education and nurturing future leaders since establishment.", help_text="Short description displayed in footer below motto")
    footer_text = models.TextField(blank=True, default="")

    # Social Media
    facebook_url = models.URLField(blank=True, default="")
    instagram_url = models.URLField(blank=True, default="")
    twitter_url = models.URLField(blank=True, default="")
    youtube_url = models.URLField(blank=True, default="")
    linkedin_url = models.URLField(blank=True, default="")
    google_maps_link = models.URLField(blank=True, default="", help_text="Link to Google Maps location")
    
    # Operating Hours
    school_hours = models.TextField(blank=True, default="", help_text="School hours (JSON or plain text)")
    office_hours = models.TextField(blank=True, default="", help_text="Office hours (JSON or plain text)")

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Settings"

    def save(self, *args, **kwargs):
        if self.school_logo:
            self.school_logo = compress_image(self.school_logo)
        if self.favicon:
            self.favicon = compress_image(self.favicon)
        super().save(*args, **kwargs)


class VisionMission(SingletonTenantModel):
    """
    Vision and Mission.
    """
    vision_title = models.CharField(max_length=255, default="Our Vision")
    vision_content = models.TextField(blank=True, default="")
    
    mission_title = models.CharField(max_length=255, default="Our Mission")
    mission_content = models.TextField(blank=True, default="")
    
    values_title = models.CharField(max_length=255, default="Core Values")
    values_content = models.TextField(blank=True, default="")

    class Meta:
        verbose_name = "Vision & Mission"
        verbose_name_plural = "Vision & Mission"

    def __str__(self):
        return "Vision & Mission"


class PrincipalMessage(SingletonTenantModel):
    """
    Principal/Director message.
    """
    name = models.CharField(max_length=255, default="Principal Name")
    title = models.CharField(max_length=100, default="Principal")
    photo = models.ImageField(upload_to=principal_upload_path, blank=True, null=True)
    message = models.TextField(blank=True, default="")
    qualification = models.CharField(max_length=255, blank=True, default="")

    class Meta:
        verbose_name = "Principal Message"
        verbose_name_plural = "Principal Message"

    def __str__(self):
        return f"Message from {self.name}"

    def save(self, *args, **kwargs):
        if self.photo:
            self.photo = compress_image(self.photo)
        super().save(*args, **kwargs)


class QuickLink(models.Model):
    """
    Quick links for footer/sidebar.
    """
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    open_in_new_tab = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']
        verbose_name = "Quick Link"
        verbose_name_plural = "Quick Links"

    def __str__(self):
        return self.title


class Facility(TenantAwareModel):
    """School facilities."""
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    short_description = models.TextField(default="", help_text="Brief description for cards")
    long_description = models.TextField(blank=True, default="", help_text="Detailed description")
    icon = models.CharField(max_length=50, default="🏫", help_text="Emoji icon")
    cover_image = models.ImageField(upload_to=facilities_upload_path, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Facility"
        verbose_name_plural = "Facilities"

    def save(self, *args, **kwargs):
        if self.cover_image:
            self.cover_image = compress_image(self.cover_image)

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

    @property
    def description(self):
        return self.short_description
    
    @property
    def image(self):
        return self.cover_image


class FacilityImage(TenantAwareModel):
    """Gallery images for a facility."""
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to=facilities_gallery_upload_path)
    caption = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Facility Image"
        verbose_name_plural = "Facility Images"

    def save(self, *args, **kwargs):
        if self.image:
            self.image = compress_image(self.image)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.facility.name} - Image {self.order}"


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
        verbose_name = "Achievement"
        verbose_name_plural = "Achievements"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.image:
            self.image = compress_image(self.image)
        super().save(*args, **kwargs)


class Testimonial(TenantAwareModel):
    """Student/Parent testimonials."""
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=100, help_text="e.g., Parent, Alumni, Student")
    photo = models.ImageField(upload_to=testimonials_upload_path, blank=True, null=True)
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5, help_text="Rating out of 5")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return f"{self.name} - {self.role}"

    def save(self, *args, **kwargs):
        if self.photo:
            self.photo = compress_image(self.photo)
        super().save(*args, **kwargs)


class GeneralInfo(TenantAwareModel):
    """General information items for public disclosure."""
    title = models.CharField(max_length=255)
    value = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "General Info"
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
        verbose_name = "Results & Academics"
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
        verbose_name = "Infrastructure"
        verbose_name_plural = "Infrastructure"

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
        verbose_name = "Fees"
        verbose_name_plural = "Fees"

    def __str__(self):
        return self.title


class Documentation(TenantAwareModel):
    """Documentation/certificates to display (not download)."""
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to=documentation_upload_path, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Documentation"
        verbose_name_plural = "Documentation"

    def __str__(self):
        return self.title


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

    def save(self, *args, **kwargs):
        if self.og_image:
            self.og_image = compress_image(self.og_image)
        super().save(*args, **kwargs)


class ContactPage(SingletonTenantModel):
    """Contact page settings."""
    hero_title = models.CharField(max_length=255, default="Contact Us")
    hero_subtitle = models.TextField(blank=True)
    map_embed_code = models.TextField(blank=True, help_text="Google Maps embed iframe code")

    class Meta:
        verbose_name = "Contact Page"
        verbose_name_plural = "Contact Page"

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
        verbose_name = "Contact Submission"
        verbose_name_plural = "Contact Submissions"

    def __str__(self):
        return f"{self.name} - {self.subject}"

# About Page Models

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
        verbose_name_plural = "About Page"

    def __str__(self):
        return "About Page"

    def save(self, *args, **kwargs):
        if self.history_image:
            self.history_image = compress_image(self.history_image)
        super().save(*args, **kwargs)


class TimelineEvent(TenantAwareModel):
    """Timeline events for school history."""
    year = models.CharField(max_length=20)
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to=about_timeline_upload_path, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'year']
        verbose_name = "Timeline Event"
        verbose_name_plural = "Timeline Events"

    def __str__(self):
        return f"{self.year} - {self.title}"

    def save(self, *args, **kwargs):
        if self.image:
            self.image = compress_image(self.image)
        super().save(*args, **kwargs)


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
        verbose_name = "Management Member"
        verbose_name_plural = "Management Members"

    def __str__(self):
        return f"{self.name} - {self.position}"

    def save(self, *args, **kwargs):
        if self.photo:
            self.photo = compress_image(self.photo)
        super().save(*args, **kwargs)
