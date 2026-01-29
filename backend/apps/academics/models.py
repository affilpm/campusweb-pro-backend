from django.db import models
from apps.core.models import TenantAwareModel, SingletonTenantModel
from apps.core.utils import academics_upload_path, compress_image

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
        verbose_name = "Class Category"
        verbose_name_plural = "Class Categories"

    def save(self, *args, **kwargs):
        if self.image:
            self.image = compress_image(self.image)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Subject(TenantAwareModel):
    """Subjects offered."""
    categories = models.ManyToManyField(ClassCategory, related_name='subjects')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True) # Ensure icon exists and is char
    is_core = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"

    def __str__(self):
        return self.name


class AcademicsPage(SingletonTenantModel):
    """Academics page settings."""
    hero_title = models.CharField(max_length=255, default="Academics")
    hero_subtitle = models.TextField(blank=True)
    hero_image = models.ImageField(upload_to=academics_upload_path, blank=True, null=True)
    overview_title = models.CharField(max_length=255, default="Academic Excellence")
    overview_content = models.TextField(blank=True)
    
    # Curriculum
    curriculum_title = models.CharField(max_length=255, default="Our Curriculum")
    curriculum_content = models.TextField(blank=True)
    curriculum_image = models.ImageField(upload_to=academics_upload_path, blank=True, null=True)
    
    # Methodology
    methodology_title = models.CharField(max_length=255, default="Our Teaching Methodology")
    methodology_content = models.TextField(blank=True)
    
    # Calendar
    calendar_title = models.CharField(max_length=255, default="Academic Calendar")
    calendar_file = models.FileField(upload_to=academics_upload_path, blank=True, null=True)

    class Meta:
        verbose_name = "Academics Page"
        verbose_name_plural = "Academics Page"

    def save(self, *args, **kwargs):
        if self.hero_image:
            self.hero_image = compress_image(self.hero_image)
        if self.curriculum_image:
            self.curriculum_image = compress_image(self.curriculum_image)
        super().save(*args, **kwargs)

    def __str__(self):
        return "Academics Page"
