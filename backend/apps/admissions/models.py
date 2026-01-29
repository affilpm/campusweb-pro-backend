from django.db import models
from apps.core.models import TenantAwareModel, SingletonTenantModel
from apps.core.utils import admissions_upload_path

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
        verbose_name_plural = "Admission Settings"

    def __str__(self):
        return "Admission Settings"


class AdmissionStep(TenantAwareModel):
    """Steps in admission process."""
    title = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.CharField(max_length=50, default="📝")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Admission Step"
        verbose_name_plural = "Admission Steps"

    def __str__(self):
        return f"Step {self.order}: {self.title}"
