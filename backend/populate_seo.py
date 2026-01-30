
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.school_info.models import PageSEO

def populate_seo():
    pages = [
        {
            "page_slug": "home",
            "title": "Home | Sunrise Public School",
            "meta_description": "Welcome to Sunrise Public School. Creating global citizens through holistic education.",
            "meta_keywords": "school, education, sunrise, public school, best school"
        },
        {
            "page_slug": "about",
            "title": "About Us | Sunrise Public School",
            "meta_description": "Learn about our history, mission, vision, and the leadership team driving excellence.",
            "meta_keywords": "about us, history, mission, vision, principal"
        },
        {
            "page_slug": "admissions",
            "title": "Admissions | Sunrise Public School",
            "meta_description": "Join our family. Check admission criteria, process, and apply online today.",
            "meta_keywords": "admissions, apply online, school admission, nursery admission"
        },
        {
            "page_slug": "academics",
            "title": "Academics | Sunrise Public School",
            "meta_description": "Explore our curriculum, teaching methodology, and academic calendar.",
            "meta_keywords": "academics, curriculum, cbse, syllabus, calendar"
        },
        {
            "page_slug": "contact",
            "title": "Contact Us | Sunrise Public School",
            "meta_description": "Get in touch with us. Address, phone number, email, and location map.",
            "meta_keywords": "contact, address, phone, email, location"
        },
        {
            "page_slug": "notices",
            "title": "Notices & Circulars | Sunrise Public School",
            "meta_description": "Stay updated with the latest school announcements, circulars, and news.",
            "meta_keywords": "notices, circulars, news, announcements, updates"
        },
        {
            "page_slug": "events",
            "title": "School Events | Sunrise Public School",
            "meta_description": "Upcoming events, competitions, and celebrations at Sunrise Public School.",
            "meta_keywords": "events, calendar, sports day, annual function, fest"
        },
        {
            "page_slug": "gallery",
            "title": "Photo Gallery | Sunrise Public School",
            "meta_description": "Glimpses of life at our school. Photos of events, campus, and students.",
            "meta_keywords": "gallery, photos, images, campus life, memories"
        },
        {
            "page_slug": "facilities",
            "title": "Campus Facilities | Sunrise Public School",
            "meta_description": "World-class infrastructure including smart labs, library, and sports complex.",
            "meta_keywords": "facilities, infrastructure, labs, library, sports"
        },
        {
            "page_slug": "documents",
            "title": "Public Disclosure | Sunrise Public School",
            "meta_description": "Mandatory public disclosures, certificates, and official documents.",
            "meta_keywords": "public disclosure, documents, cbse disclosure, certificates"
        }
    ]

    for page_data in pages:
        obj, created = PageSEO.objects.get_or_create(
            page_slug=page_data['page_slug'],
            defaults=page_data
        )
        status = "Created" if created else "Skipped (Exists)"
        print(f"{status}: {page_data['page_slug']}")

if __name__ == '__main__':
    populate_seo()
