"""
Content forms for public and admin use.
"""

from django import forms
from .models import (
    ContactSubmission, Notice, Event, Facility, Achievement,
    Testimonial, GalleryCategory, GalleryImage, SiteSettings,
    HeroSection, HomeAboutSection, PrincipalMessage, VisionMission,
    AcademicsPage, AdmissionSettings, AdmissionStep, AboutPage,
    TimelineEvent, ManagementMember, GeneralInfo, ContactPage, PageSEO
)


# --- Public Forms ---

class ContactForm(forms.ModelForm):
    """Contact form for public visitors."""
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all',
                'placeholder': 'Your name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all',
                'placeholder': 'your@email.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all',
                'placeholder': 'Your phone number'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all',
                'placeholder': 'Message subject'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all resize-none',
                'placeholder': 'How can we help you?',
                'rows': 5
            }),
        }


# --- Admin Forms ---

class SiteSettingsForm(forms.ModelForm):
    """Form for site settings."""
    class Meta:
        model = SiteSettings
        fields = '__all__'
        widgets = {
            'school_address': forms.Textarea(attrs={'rows': 3}),
            'school_phone': forms.Textarea(attrs={'rows': 2, 'help_text': 'Multiple phones separated by commas'}),
            'footer_text': forms.Textarea(attrs={'rows': 3}),
        }


class HeroSectionForm(forms.ModelForm):
    """Form for hero section."""
    class Meta:
        model = HeroSection
        fields = '__all__'
        widgets = {
            'subtitle': forms.Textarea(attrs={'rows': 2}),
        }


class NoticeForm(forms.ModelForm):
    """Form for notices."""
    class Meta:
        model = Notice
        fields = ['title', 'content', 'attachment', 'is_important', 'status', 'publish_date', 'expiry_date']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
            'publish_date': forms.DateInput(attrs={'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }


class EventForm(forms.ModelForm):
    """Form for events."""
    class Meta:
        model = Event
        fields = ['title', 'excerpt', 'content', 'image', 'event_date', 'is_featured', 'status']
        widgets = {
            'excerpt': forms.Textarea(attrs={'rows': 2}),
            'content': forms.Textarea(attrs={'rows': 8}),
            'event_date': forms.DateInput(attrs={'type': 'date'}),
        }


class FacilityForm(forms.ModelForm):
    """Form for facilities."""
    class Meta:
        model = Facility
        fields = ['name', 'short_description', 'long_description', 'icon', 'cover_image', 'order', 'is_active']
        widgets = {
            'short_description': forms.Textarea(attrs={'rows': 2}),
            'long_description': forms.Textarea(attrs={'rows': 5}),
        }


class AchievementForm(forms.ModelForm):
    """Form for achievements."""
    class Meta:
        model = Achievement
        fields = ['title', 'description', 'image', 'year', 'order', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class TestimonialForm(forms.ModelForm):
    """Form for testimonials."""
    class Meta:
        model = Testimonial
        fields = ['name', 'role', 'photo', 'content', 'rating', 'order', 'is_active']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }


class GalleryCategoryForm(forms.ModelForm):
    """Form for gallery categories."""
    class Meta:
        model = GalleryCategory
        fields = ['name', 'order']


class GalleryImageForm(forms.ModelForm):
    """Form for gallery images."""
    class Meta:
        model = GalleryImage
        fields = ['category', 'title', 'image', 'caption', 'is_featured', 'order']


class AboutPageForm(forms.ModelForm):
    """Form for about page."""
    class Meta:
        model = AboutPage
        fields = '__all__'
        widgets = {
            'hero_subtitle': forms.Textarea(attrs={'rows': 2}),
            'history_content': forms.Textarea(attrs={'rows': 5}),
            'infrastructure_content': forms.Textarea(attrs={'rows': 4}),
        }


class TimelineEventForm(forms.ModelForm):
    """Form for timeline events."""
    class Meta:
        model = TimelineEvent
        fields = ['year', 'title', 'description', 'image', 'order']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class ManagementMemberForm(forms.ModelForm):
    """Form for management members."""
    class Meta:
        model = ManagementMember
        fields = ['name', 'position', 'photo', 'bio', 'email', 'phone', 'order', 'is_active']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }


class PageSEOForm(forms.ModelForm):
    """Form for page SEO."""
    class Meta:
        model = PageSEO
        fields = ['page_slug', 'title', 'meta_description', 'meta_keywords', 'og_image']
        widgets = {
            'meta_description': forms.Textarea(attrs={'rows': 3}),
        }
