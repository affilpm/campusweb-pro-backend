"""
Core utilities for file uploads.
"""

import uuid
import os
import io
from PIL import Image
from django.core.files.base import ContentFile
from django.utils.text import slugify

def get_filename_ext(filename):
    return filename.split('.')[-1]


def unique_upload_path(instance, filename, folder='uploads'):
    """Generate unique upload path for files."""
    ext = get_filename_ext(filename)
    filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join(folder, filename)


def logos_upload_path(instance, filename):
    return unique_upload_path(instance, filename, 'site/logos')


def hero_upload_path(instance, filename):
    return unique_upload_path(instance, filename, 'site/hero')


def about_upload_path(instance, filename):
    return unique_upload_path(instance, filename, 'site/about')


def principal_upload_path(instance, filename):
    name_slug = slugify(instance.name) if instance.name else 'principal'
    return unique_upload_path(instance, filename, f'site/principal/{name_slug}')


def notices_upload_path(instance, filename):
    folder = 'communication/notices'
    if hasattr(instance, 'publish_date') and instance.publish_date:
        folder = f"communication/notices/{instance.publish_date.strftime('%Y/%m')}"
    return unique_upload_path(instance, filename, folder)


def events_upload_path(instance, filename):
    folder = 'communication/events'
    if hasattr(instance, 'event_date') and instance.event_date:
        folder = f"communication/events/{instance.event_date.strftime('%Y/%m')}"
    return unique_upload_path(instance, filename, folder)


def gallery_upload_path(instance, filename):
    # instance is GalleryImage
    folder = 'gallery/uncategorized'
    if hasattr(instance, 'category') and instance.category:
        cat_slug = slugify(instance.category.name)
        folder = f'gallery/{cat_slug}'
    return unique_upload_path(instance, filename, folder)


def facilities_upload_path(instance, filename):
    # instance is Facility
    name_slug = instance.slug or slugify(instance.name) or 'new-facility'
    return unique_upload_path(instance, filename, f'facilities/{name_slug}/cover')


def facilities_gallery_upload_path(instance, filename):
    # instance is FacilityImage
    folder = 'facilities/gallery'
    if instance.facility:
        fac_slug = instance.facility.slug or slugify(instance.facility.name)
        folder = f'facilities/{fac_slug}/gallery'
    return unique_upload_path(instance, filename, folder)


def academics_upload_path(instance, filename):
    # Differentiate between AcademicsPage (singleton) and ClassCategory/Subject
    folder = 'academics/general'
    if instance.__class__.__name__ == 'AcademicsPage':
        folder = 'academics/page'
    elif hasattr(instance, 'name'):
        slug = slugify(instance.name)
        folder = f'academics/categories/{slug}'
    return unique_upload_path(instance, filename, folder)


def about_timeline_upload_path(instance, filename):
    folder = 'site/about/timeline'
    if instance.year:
        name_part = slugify(instance.title) if instance.title else 'event'
        folder = f'site/about/timeline/{instance.year}_{name_part}'
    return unique_upload_path(instance, filename, folder)


def about_management_upload_path(instance, filename):
    name_slug = slugify(instance.name) if instance.name else 'member'
    return unique_upload_path(instance, filename, f'site/about/management/{name_slug}')


def admissions_upload_path(instance, filename):
    return unique_upload_path(instance, filename, 'admissions/page')


def testimonials_upload_path(instance, filename):
    name_slug = slugify(instance.name) if instance.name else 'testimonial'
    return unique_upload_path(instance, filename, f'testimonials/{name_slug}')


def downloads_upload_path(instance, filename):
    title_slug = slugify(instance.title) if instance.title else 'file'
    return unique_upload_path(instance, filename, f'downloads/{title_slug}')


def documentation_upload_path(instance, filename):
    title_slug = slugify(instance.title) if instance.title else 'doc'
    return unique_upload_path(instance, filename, f'documentation/{title_slug}')


def achievements_upload_path(instance, filename):
    title_slug = slugify(instance.title) if instance.title else 'achievement'
    return unique_upload_path(instance, filename, f'achievements/{title_slug}')


def seo_upload_path(instance, filename):
    page = instance.page_slug or 'unknown'
    return unique_upload_path(instance, filename, f'seo/{page}')


def results_upload_path(instance, filename):
    title_slug = slugify(instance.title) if instance.title else 'result'
    return unique_upload_path(instance, filename, f'academics/results/{title_slug}')

def compress_image(image, max_size=(1920, 1080), quality=85):
    """
    Compresses an image using Pillow.
    - Resizes to max_size (keeping aspect ratio)
    - Converts to WebP (optimized)
    - Returns a ContentFile
    """
    if not image:
        return image

    # Optimization: Skip if it's already a saved FieldFile or similar (not a fresh upload)
    # Uploaded files usually have a 'file' attribute that is a BytesIO/TemporaryFile 
    # and has a 'content_type' attribute. FieldFiles are just path-like.
    if hasattr(image, 'file') and not hasattr(image.file, 'content_type'):
        return image

    try:
        img = Image.open(image)
        
        # Convert RGBA to RGB if needed (for JPEG/WebP)
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
            
        # Resize if larger than max_size
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Save to buffer
        buffer = io.BytesIO()
        img.save(buffer, format='WEBP', quality=quality, optimize=True)
        buffer.seek(0)
        
        # Create new filename
        original_name = image.name.split('.')[0]
        new_name = f"{original_name}.webp"
        
        return ContentFile(buffer.read(), name=new_name)
    except Exception as e:
        print(f"Error compressing image: {e}")
        return image
