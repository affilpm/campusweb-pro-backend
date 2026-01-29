from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from apps.core.models import TenantAwareModel
from apps.core.utils import notices_upload_path, events_upload_path, compress_image

class Notice(TenantAwareModel):
    """
    School notices and announcements.
    """
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'
        ARCHIVED = 'archived', 'Archived'

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    content = models.TextField()
    attachment = models.FileField(upload_to=notices_upload_path, blank=True, null=True)
    is_important = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    publish_date = models.DateField(default=timezone.now)
    expiry_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['-is_important', '-publish_date', '-created_at']
        verbose_name = "Notice"
        verbose_name_plural = "Notices"

    def save(self, *args, **kwargs):
        if self.attachment:
            if self.attachment.name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                try:
                    self.attachment = compress_image(self.attachment)
                except Exception:
                    pass

        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Notice.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Event(TenantAwareModel):
    """
    School events and news.
    """
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
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def save(self, *args, **kwargs):
        if self.image:
            self.image = compress_image(self.image)

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
