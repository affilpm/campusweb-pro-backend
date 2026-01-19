"""
Public site views - server-side rendered pages.
Replaces Next.js pages with direct Django template rendering.
"""

from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.db.models import Prefetch

from content.models import (
    SiteSettings, HeroSection, VisionMission, HomeAboutSection, PrincipalMessage,
    QuickLink, Notice, Event, GalleryCategory, GalleryImage, Facility,
    Achievement, Testimonial, AcademicHighlight, AcademicsPage, ClassCategory,
    AdmissionSettings, AdmissionStep, AboutPage, TimelineEvent, ManagementMember,
    GeneralInfo, ResultsAcademics, Infrastructure, Fees, ContactPage,
    ContactSubmission, PageSEO, Documentation
)
from content.forms import ContactForm


def get_seo(page_slug):
    """Get SEO data for a page."""
    try:
        return PageSEO.objects.get(page_slug=page_slug)
    except PageSEO.DoesNotExist:
        return None


def home(request):
    """
    Homepage view - replaces /api/public/home/ + React rendering.
    All data is loaded server-side and passed to template.
    """
    context = {
        'hero': HeroSection.objects.first(),
        'about': HomeAboutSection.objects.first(),
        'principal': PrincipalMessage.objects.first(),
        'vision_mission': VisionMission.objects.first(),
        'notices': Notice.objects.filter(status='published').order_by('-is_important', '-publish_date')[:5],
        'events': Event.objects.filter(status='published').order_by('-is_featured', '-event_date')[:6],
        'gallery': GalleryImage.objects.filter(is_featured=True).select_related('category')[:8],
        'facilities': Facility.objects.filter(is_active=True).order_by('order')[:6],
        'achievements': Achievement.objects.filter(is_active=True).order_by('order'),
        'testimonials': Testimonial.objects.filter(is_active=True).order_by('order'),
        'academics': AcademicHighlight.objects.filter(is_active=True).order_by('order'),
        'general_info': GeneralInfo.objects.filter(is_active=True).order_by('order')[:6],
        'seo': get_seo('home'),
    }
    return render(request, 'public/home.html', context)


def about(request):
    """About page view."""
    about_page = AboutPage.objects.first()
    context = {
        'page': about_page,
        'about_section': HomeAboutSection.objects.first(),
        'vision_mission': VisionMission.objects.first(),
        'principal': PrincipalMessage.objects.first(),
        'timeline': TimelineEvent.objects.all().order_by('order', 'year'),
        'management': ManagementMember.objects.filter(is_active=True).order_by('order'),
        'facilities': Facility.objects.filter(is_active=True).order_by('order'),
        'seo': get_seo('about'),
    }
    return render(request, 'public/about.html', context)


def academics(request):
    """Academics page view."""
    academics_page = AcademicsPage.objects.first()
    class_categories = ClassCategory.objects.filter(is_active=True).prefetch_related(
        Prefetch('subjects', queryset=__import__('content.models', fromlist=['Subject']).Subject.objects.filter(is_active=True).order_by('order'))
    ).order_by('order')
    
    context = {
        'page': academics_page,
        'class_categories': class_categories,
        'seo': get_seo('academics'),
    }
    return render(request, 'public/academics.html', context)


def admissions(request):
    """Admissions page view."""
    admission_settings = AdmissionSettings.objects.first()
    context = {
        'page': admission_settings,
        'steps': AdmissionStep.objects.all().order_by('order'),
        'seo': get_seo('admissions'),
    }
    return render(request, 'public/admissions.html', context)


@require_http_methods(["GET", "POST"])
def contact(request):
    """Contact page with form submission."""
    contact_page = ContactPage.objects.first()
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            form = ContactForm()  # Reset form
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()
    
    context = {
        'page': contact_page,
        'form': form,
        'seo': get_seo('contact'),
    }
    return render(request, 'public/contact.html', context)


def facilities(request):
    """Facilities page view."""
    context = {
        'facilities': Facility.objects.filter(is_active=True).prefetch_related('gallery_images').order_by('order'),
        'seo': get_seo('facilities'),
    }
    return render(request, 'public/facilities.html', context)


def facility_detail(request, slug):
    """Individual facility detail page."""
    facility = get_object_or_404(Facility, slug=slug, is_active=True)
    context = {
        'facility': facility,
        'gallery': facility.gallery_images.filter(is_active=True).order_by('order'),
    }
    return render(request, 'public/facility_detail.html', context)


def gallery(request):
    """Gallery page view."""
    categories = GalleryCategory.objects.prefetch_related(
        Prefetch('images', queryset=GalleryImage.objects.order_by('-is_featured', 'order'))
    ).order_by('order')
    
    context = {
        'categories': categories,
        'seo': get_seo('gallery'),
    }
    return render(request, 'public/gallery.html', context)


def notices(request):
    """Notices listing page."""
    context = {
        'notices': Notice.objects.filter(status='published').order_by('-is_important', '-publish_date'),
        'seo': get_seo('notices'),
    }
    return render(request, 'public/notices.html', context)


def notice_detail(request, pk):
    """Individual notice detail page."""
    notice = get_object_or_404(Notice, pk=pk, status='published')
    context = {
        'notice': notice,
    }
    return render(request, 'public/notice_detail.html', context)


def events(request):
    """Events listing page."""
    context = {
        'events': Event.objects.filter(status='published').order_by('-is_featured', '-event_date'),
        'seo': get_seo('events'),
    }
    return render(request, 'public/events.html', context)


def event_detail(request, slug):
    """Individual event detail page."""
    event = get_object_or_404(Event, slug=slug, status='published')
    context = {
        'event': event,
    }
    return render(request, 'public/event_detail.html', context)


def public_disclosure(request):
    """Public disclosure page."""
    context = {
        'general_info': GeneralInfo.objects.filter(is_active=True).order_by('order'),
        'results': ResultsAcademics.objects.filter(is_active=True).order_by('order'),
        'infrastructure': Infrastructure.objects.filter(is_active=True).order_by('order'),
        'fees': Fees.objects.filter(is_active=True).order_by('order'),
        'documents': Documentation.objects.filter(is_active=True).order_by('order'),
        'seo': get_seo('public-disclosure'),
    }
    return render(request, 'public/public_disclosure.html', context)
