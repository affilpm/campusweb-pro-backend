"""
Core utilities for file uploads.
"""

import uuid
import os


def unique_upload_path(instance, filename, folder='uploads'):
    """Generate unique upload path for files."""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join(folder, filename)


def logos_upload_path(instance, filename):
    return unique_upload_path(instance, filename, 'logos')


def hero_upload_path(instance, filename):
    return unique_upload_path(instance, filename, 'hero')


def about_upload_path(instance, filename):
    return unique_upload_path(instance, filename, 'about')


def principal_upload_path(instance, filename):
    return unique_upload_path(instance, filename, 'principal')


def notices_upload_path(instance, filename):
    return unique_upload_path(instance, filename, 'notices')


def events_upload_path(instance, filename):
    return unique_upload_path(instance, filename, 'events')


def gallery_upload_path(instance, filename):
    return unique_upload_path(instance, filename, 'gallery')


def facilities_upload_path(instance, filename):
    return unique_upload_path(instance, filename, 'facilities')


def facilities_gallery_upload_path(instance, filename):
    return unique_upload_path(instance, filename, 'facilities/gallery')


def academics_upload_path(instance, filename):
    return unique_upload_path(instance, filename, 'academics')


def about_timeline_upload_path(instance, filename):
    return unique_upload_path(instance, filename, 'about/timeline')


def about_management_upload_path(instance, filename):
    return unique_upload_path(instance, filename, 'about/management')


def admissions_upload_path(instance, filename):
    return unique_upload_path(instance, filename, 'admissions')


def testimonials_upload_path(instance, filename):
    return unique_upload_path(instance, filename, 'testimonials')


def downloads_upload_path(instance, filename):
    return unique_upload_path(instance, filename, 'downloads')


def documentation_upload_path(instance, filename):
    return unique_upload_path(instance, filename, 'documentation')


def achievements_upload_path(instance, filename):
    return unique_upload_path(instance, filename, 'achievements')


def seo_upload_path(instance, filename):
    return unique_upload_path(instance, filename, 'seo')


def results_upload_path(instance, filename):
    return unique_upload_path(instance, filename, 'results')
