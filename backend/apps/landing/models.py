from django.db import models
from apps.core.models import SingletonTenantModel, TenantAwareModel
from apps.core.utils import hero_upload_path, about_upload_path, compress_image

class HeroSection(SingletonTenantModel):
    """
    Homepage hero section.
    """
    title = models.CharField(max_length=255, default="Welcome to Our School")
    subtitle = models.TextField(blank=True, default="Empowering Minds, Shaping Futures")
    image = models.ImageField(upload_to=hero_upload_path, blank=True, null=True)
    cta_text = models.CharField(max_length=50, default="Admissions Open")
    cta_link = models.CharField(max_length=255, default="/admissions")

    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Section"

    def save(self, *args, **kwargs):
        if self.image:
            self.image = compress_image(self.image)
        super().save(*args, **kwargs)

    def __str__(self):
        return "Hero Section"


class HomeAboutSection(SingletonTenantModel):
    """
    Homepage about section.
    """
    title = models.CharField(max_length=255, default="About Us")
    content = models.TextField(blank=True, default="")
    image = models.ImageField(upload_to=about_upload_path, blank=True, null=True)
    
    # Stats
    established_year = models.PositiveIntegerField(default=2000)
    students_count = models.CharField(max_length=50, default="500+")
    teachers_count = models.CharField(max_length=50, default="30+")

    class Meta:
        verbose_name = "About Section (Home)"
        verbose_name_plural = "About Section (Home)"

    def save(self, *args, **kwargs):
        if self.image:
            self.image = compress_image(self.image)
        super().save(*args, **kwargs)

    def __str__(self):
        return "About Section (Home)"


class AcademicHighlight(TenantAwareModel):
    """Academic highlights for homepage."""
    title = models.CharField(max_length=100)
    value = models.CharField(max_length=50)
    icon = models.CharField(max_length=50, default="📚")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Academic Highlight"
        verbose_name_plural = "Academic Highlights"

    def __str__(self):
        return self.title
