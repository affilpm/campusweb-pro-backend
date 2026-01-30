from django.db import models
from django.utils.text import slugify
from apps.core.models import TenantAwareModel
from apps.core.utils import gallery_upload_path, compress_image

class GalleryCategory(TenantAwareModel):
    """Gallery categories."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Gallery Category"
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
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery Images"

    def save(self, *args, **kwargs):
        if self.image:
            self.image = compress_image(self.image)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title or f"Gallery Image {self.pk}"
