"""
Management command to create initial site data.
"""

from django.core.management.base import BaseCommand
from content.models import (
    SiteSettings, HeroSection, VisionMission, HomeAboutSection,
    PrincipalMessage, AcademicsPage, AdmissionSettings, AboutPage, ContactPage
)


class Command(BaseCommand):
    help = 'Creates initial site data (singleton models)'

    def handle(self, *args, **options):
        # Create singleton models if they don't exist
        models = [
            (SiteSettings, 'Site Settings'),
            (HeroSection, 'Hero Section'),
            (VisionMission, 'Vision & Mission'),
            (HomeAboutSection, 'Home About Section'),
            (PrincipalMessage, 'Principal Message'),
            (AcademicsPage, 'Academics Page'),
            (AdmissionSettings, 'Admission Settings'),
            (AboutPage, 'About Page'),
            (ContactPage, 'Contact Page'),
        ]
        
        for model_class, name in models:
            obj, created = model_class.objects.get_or_create(pk=1)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created {name}'))
            else:
                self.stdout.write(f'{name} already exists')
        
        self.stdout.write(self.style.SUCCESS('Initial data setup complete!'))
