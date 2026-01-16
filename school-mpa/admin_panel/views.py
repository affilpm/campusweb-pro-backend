"""
Admin panel views.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from authentication.decorators import admin_required, role_required

from content.models import (
    SiteSettings, HeroSection, VisionMission, HomeAboutSection, PrincipalMessage,
    Notice, Event, GalleryCategory, GalleryImage, Facility,
    Achievement, Testimonial, AcademicsPage, AdmissionSettings, AdmissionStep,
    AboutPage, TimelineEvent, ManagementMember, ContactPage, ContactSubmission, PageSEO
)
from content.forms import (
    SiteSettingsForm, HeroSectionForm, NoticeForm, EventForm,
    FacilityForm, AchievementForm, TestimonialForm, GalleryCategoryForm,
    GalleryImageForm, AboutPageForm, TimelineEventForm, ManagementMemberForm, PageSEOForm
)


@admin_required
def dashboard(request):
    """Admin dashboard with overview stats."""
    context = {
        'notices_count': Notice.objects.filter(status='published').count(),
        'events_count': Event.objects.filter(status='published').count(),
        'contact_submissions': ContactSubmission.objects.filter(is_read=False).count(),
        'recent_notices': Notice.objects.order_by('-created_at')[:5],
        'recent_submissions': ContactSubmission.objects.order_by('-created_at')[:5],
    }
    return render(request, 'admin/dashboard.html', context)


# --- Site Settings ---
@admin_required
def site_settings(request):
    """Manage site settings."""
    instance = SiteSettings.objects.first()
    if request.method == 'POST':
        form = SiteSettingsForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Site settings updated successfully.')
            return redirect('admin-settings')
    else:
        form = SiteSettingsForm(instance=instance)
    return render(request, 'admin/settings/site_settings.html', {'form': form})


# --- Notices CRUD ---
@admin_required
def notices_list(request):
    """List all notices."""
    notices = Notice.objects.all().order_by('-created_at')
    paginator = Paginator(notices, 20)
    page = request.GET.get('page', 1)
    notices = paginator.get_page(page)
    return render(request, 'admin/notices/list.html', {'notices': notices})


@admin_required
def notice_create(request):
    """Create a new notice."""
    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notice created successfully.')
            return redirect('admin-notices')
    else:
        form = NoticeForm()
    return render(request, 'admin/notices/form.html', {'form': form, 'title': 'Create Notice'})


@admin_required
def notice_edit(request, pk):
    """Edit an existing notice."""
    notice = get_object_or_404(Notice, pk=pk)
    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES, instance=notice)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notice updated successfully.')
            return redirect('admin-notices')
    else:
        form = NoticeForm(instance=notice)
    return render(request, 'admin/notices/form.html', {'form': form, 'title': 'Edit Notice', 'object': notice})


@admin_required
def notice_delete(request, pk):
    """Delete a notice."""
    notice = get_object_or_404(Notice, pk=pk)
    if request.method == 'POST':
        notice.delete()
        messages.success(request, 'Notice deleted successfully.')
        return redirect('admin-notices')
    return render(request, 'admin/confirm_delete.html', {'object': notice, 'type': 'Notice'})


# --- Events CRUD ---
@admin_required
def events_list(request):
    events = Event.objects.all().order_by('-created_at')
    paginator = Paginator(events, 20)
    page = request.GET.get('page', 1)
    events = paginator.get_page(page)
    return render(request, 'admin/events/list.html', {'events': events})


@admin_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event created successfully.')
            return redirect('admin-events')
    else:
        form = EventForm()
    return render(request, 'admin/events/form.html', {'form': form, 'title': 'Create Event'})


@admin_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully.')
            return redirect('admin-events')
    else:
        form = EventForm(instance=event)
    return render(request, 'admin/events/form.html', {'form': form, 'title': 'Edit Event', 'object': event})


@admin_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully.')
        return redirect('admin-events')
    return render(request, 'admin/confirm_delete.html', {'object': event, 'type': 'Event'})


# --- Contact Submissions ---
@admin_required
def contact_submissions_list(request):
    submissions = ContactSubmission.objects.all().order_by('-created_at')
    paginator = Paginator(submissions, 20)
    page = request.GET.get('page', 1)
    submissions = paginator.get_page(page)
    return render(request, 'admin/contact/list.html', {'submissions': submissions})


@admin_required
def contact_submission_detail(request, pk):
    submission = get_object_or_404(ContactSubmission, pk=pk)
    if not submission.is_read:
        submission.is_read = True
        submission.save()
    return render(request, 'admin/contact/detail.html', {'submission': submission})


@admin_required
def contact_submission_delete(request, pk):
    submission = get_object_or_404(ContactSubmission, pk=pk)
    if request.method == 'POST':
        submission.delete()
        messages.success(request, 'Submission deleted.')
        return redirect('admin-contact-submissions')
    return render(request, 'admin/confirm_delete.html', {'object': submission, 'type': 'Contact Submission'})
