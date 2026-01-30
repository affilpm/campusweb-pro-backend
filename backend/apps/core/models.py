"""
Core models - Base classes for all apps.
"""

from django.db import models


class TenantAwareModel(models.Model):
    """
    Base model for all tenant-specific data.
    
    Currently: Single-tenant mode (no tenant field)
    Future SaaS: Add `school = ForeignKey('tenants.School')`
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class SingletonTenantModel(TenantAwareModel):
    """
    Singleton per tenant. Currently just a global singleton.
    Future SaaS: One instance per school.
    """
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        pass  # Prevent deletion of singleton
    
    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
