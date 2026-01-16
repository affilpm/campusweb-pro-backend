"""
Core app - Base models and utilities.
"""
from django.db import models
from django.utils import timezone


class TenantAwareModel(models.Model):
    """
    Base model with timestamps.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SingletonTenantModel(models.Model):
    """
    Base model for singleton settings (only one instance per tenant).
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_instance(cls):
        """Get or create the singleton instance."""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
