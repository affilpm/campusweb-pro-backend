"""
Context processors for global template variables.
"""
from content.models import SiteSettings, QuickLink


def site_settings(request):
    """
    Add site settings and quick links to all template contexts.
    """
    try:
        settings = SiteSettings.objects.first()
    except Exception:
        settings = None
    
    try:
        quick_links = QuickLink.objects.filter(is_active=True).order_by('order')
    except Exception:
        quick_links = []
    
    return {
        'site_settings': settings,
        'quick_links': quick_links,
    }
