"""
Core utilities - file upload paths.
"""
import uuid
from django.utils import timezone


def unique_upload_path(instance, filename):
    """Generate unique upload path with UUID."""
    ext = filename.split('.')[-1] if '.' in filename else ''
    unique_name = f"{uuid.uuid4().hex}.{ext}" if ext else uuid.uuid4().hex
    return f"uploads/{timezone.now().strftime('%Y/%m')}/{unique_name}"


def logos_upload_path(instance, filename):
    return f"logos/{unique_upload_path(instance, filename)}"


def hero_upload_path(instance, filename):
    return f"hero/{unique_upload_path(instance, filename)}"


def about_upload_path(instance, filename):
    return f"about/{unique_upload_path(instance, filename)}"


def principal_upload_path(instance, filename):
    return f"principal/{unique_upload_path(instance, filename)}"


def notices_upload_path(instance, filename):
    return f"notices/{unique_upload_path(instance, filename)}"


def events_upload_path(instance, filename):
    return f"events/{unique_upload_path(instance, filename)}"


def gallery_upload_path(instance, filename):
    return f"gallery/{unique_upload_path(instance, filename)}"


def facilities_upload_path(instance, filename):
    return f"facilities/{unique_upload_path(instance, filename)}"


def facilities_gallery_upload_path(instance, filename):
    return f"facilities/gallery/{unique_upload_path(instance, filename)}"


def achievements_upload_path(instance, filename):
    return f"achievements/{unique_upload_path(instance, filename)}"


def testimonials_upload_path(instance, filename):
    return f"testimonials/{unique_upload_path(instance, filename)}"


def documentation_upload_path(instance, filename):
    return f"documentation/{unique_upload_path(instance, filename)}"


def academics_upload_path(instance, filename):
    return f"academics/{unique_upload_path(instance, filename)}"


def admissions_upload_path(instance, filename):
    return f"admissions/{unique_upload_path(instance, filename)}"


def about_timeline_upload_path(instance, filename):
    return f"about/timeline/{unique_upload_path(instance, filename)}"


def about_management_upload_path(instance, filename):
    return f"about/management/{unique_upload_path(instance, filename)}"


def results_upload_path(instance, filename):
    return f"results/{unique_upload_path(instance, filename)}"


def seo_upload_path(instance, filename):
    return f"seo/{unique_upload_path(instance, filename)}"
