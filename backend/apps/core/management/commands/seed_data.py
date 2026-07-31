"""
Management command to seed the database with comprehensive production-quality
fictional data for Green Valley Public School, Kerala.

Usage:
    python manage.py seed_data
    python manage.py seed_data --flush   # Clear all content data first
"""
import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.school_info.models import (
    SiteSettings, VisionMission, PrincipalMessage, QuickLink,
    Facility, Achievement, Testimonial, Documentation,
    AboutPage, TimelineEvent, ManagementMember,
    GeneralInfo, ResultsAcademics, Infrastructure, Fees, PageSEO,
    FacilityImage, ContactPage, ContactSubmission
)
from apps.landing.models import HeroSection, HomeAboutSection, AcademicHighlight
from apps.communication.models import Notice, Event
from apps.gallery.models import GalleryCategory, GalleryImage
from apps.academics.models import AcademicsPage, ClassCategory, Subject
from apps.admissions.models import AdmissionSettings, AdmissionStep


class Command(BaseCommand):
    help = 'Populate database with comprehensive fictional data for Green Valley Public School'

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush',
            action='store_true',
            help='Clear all existing content data before seeding',
        )

    def handle(self, *args, **options):
        self.stdout.write('\n🏫 Seeding database for Green Valley Public School, Kerala...\n')

        if options['flush']:
            self.stdout.write(self.style.WARNING('  ⚠ Flushing existing content data...\n'))
            self._flush_content()

        # ── Global / Singleton Settings ──────────────────────────
        self.seed_site_settings()
        self.seed_hero_section()
        self.seed_home_about_section()
        self.seed_vision_mission()
        self.seed_principal_message()
        self.seed_about_page()
        self.seed_contact_page()
        self.seed_academics_page()
        self.seed_admission_settings()

        # ── Repeatable Content ───────────────────────────────────
        self.seed_quick_links()
        self.seed_academic_highlights()
        self.seed_class_categories_and_subjects()
        self.seed_admission_steps()
        self.seed_timeline_events()
        self.seed_management_members()
        self.seed_facilities()
        self.seed_achievements()
        self.seed_testimonials()
        self.seed_notices()
        self.seed_events()
        self.seed_gallery()
        self.seed_documentation()
        self.seed_contact_submissions()

        # ── Public Disclosure ────────────────────────────────────
        self.seed_general_info()
        self.seed_results_academics()
        self.seed_infrastructure()
        self.seed_fees()

        # ── SEO ──────────────────────────────────────────────────
        self.seed_seo()

        self.stdout.write(self.style.SUCCESS(
            '\n✅ Database seeded successfully for Green Valley Public School!\n'
        ))

    # ─────────────────────────────────────────────────────────────
    #  FLUSH HELPER
    # ─────────────────────────────────────────────────────────────
    def _flush_content(self):
        """Delete all user-managed content (preserves auth & system tables)."""
        models_to_flush = [
            QuickLink, AcademicHighlight, AdmissionStep,
            FacilityImage, Facility, Achievement, Testimonial,
            GalleryImage, GalleryCategory,
            Notice, Event, Documentation,
            TimelineEvent, ManagementMember,
            GeneralInfo, ResultsAcademics, Infrastructure, Fees,
            PageSEO, ContactSubmission,
        ]
        for model in models_to_flush:
            count = model.objects.all().delete()[0]
            if count:
                self.stdout.write(f'    Deleted {count} {model.__name__} records')
        # Clear M2M for Subject before deleting
        Subject.objects.all().delete()
        ClassCategory.objects.all().delete()

    # ─────────────────────────────────────────────────────────────
    #  1. SITE SETTINGS (Singleton pk=1)
    # ─────────────────────────────────────────────────────────────
    def seed_site_settings(self):
        s, _ = SiteSettings.objects.get_or_create(pk=1)
        s.school_name = "Green Valley Public School"
        s.school_motto = "Nurturing Roots, Growing Wings"
        s.school_description = (
            "Committed to providing quality education and nurturing future leaders "
            "since 1998. Green Valley Public School blends Kerala's rich academic "
            "heritage with modern pedagogical practices to shape compassionate, "
            "thinking citizens of tomorrow."
        )
        s.school_address = (
            "Green Valley Public School,\n"
            "Mangalam Road, Perumala Junction,\n"
            "Meenachil P.O., Kottayam District,\n"
            "Kerala — 686 561, India"
        )
        s.school_phone = "+91 481 253 4001, +91 481 253 4002, +91 94470 12345"
        s.school_email = "info@greenvalleyschool.edu.in"
        s.school_logo = "placeholder/gvps_logo.png"
        s.favicon = "placeholder/gvps_favicon.png"

        import json
        s.school_hours = json.dumps([
            {"day": "Monday – Friday", "time": "8:30 AM – 3:30 PM"},
            {"day": "Saturday", "time": "8:30 AM – 12:30 PM"},
            {"day": "Sunday", "time": "Closed"}
        ])
        s.office_hours = json.dumps([
            {"day": "Monday – Friday", "time": "9:00 AM – 4:30 PM"},
            {"day": "Saturday", "time": "9:00 AM – 1:00 PM"},
            {"day": "Sunday", "time": "Closed"}
        ])

        s.facebook_url = "https://facebook.com/greenvalleypublicschool"
        s.instagram_url = "https://instagram.com/gvps_official"
        s.twitter_url = "https://twitter.com/gvps_kottayam"
        s.youtube_url = "https://youtube.com/@greenvalleypublicschool"
        s.linkedin_url = "https://linkedin.com/school/green-valley-public-school"
        s.google_maps_link = (
            "https://www.google.com/maps/place/9.5916%C2%B0N+76.5222%C2%B0E"
        )

        s.footer_text = "© 2026 Green Valley Public School, Kottayam. All rights reserved."
        s.save()
        self.stdout.write('  ✓ Site Settings')

    # ─────────────────────────────────────────────────────────────
    #  2. HERO SECTION (Singleton pk=1)
    # ─────────────────────────────────────────────────────────────
    def seed_hero_section(self):
        h, _ = HeroSection.objects.get_or_create(pk=1)
        h.title = "Welcome to Green Valley Public School"
        h.subtitle = (
            "Where tradition meets innovation — empowering young minds in the "
            "heart of Kerala since 1998. Discover a campus alive with curiosity, "
            "creativity, and character."
        )
        h.image = "placeholder/hero_campus_aerial.jpg"
        h.cta_text = "Admissions Open 2026-27"
        h.cta_link = "/admissions"
        h.save()
        self.stdout.write('  ✓ Hero Section')

    # ─────────────────────────────────────────────────────────────
    #  3. HOME ABOUT SECTION (Singleton pk=1)
    # ─────────────────────────────────────────────────────────────
    def seed_home_about_section(self):
        a, _ = HomeAboutSection.objects.get_or_create(pk=1)
        a.title = "About Green Valley"
        a.content = (
            "<p>Founded in 1998 by the Green Valley Educational Trust, our school "
            "has blossomed from a modest primary school into a thriving CBSE-affiliated "
            "institution offering classes from Pre-Primary to Grade XII.</p>"
            "<p>Set against the lush Western Ghats foothills in Kottayam district, "
            "our 8-acre eco-campus provides the perfect backdrop for holistic learning — "
            "combining rigorous academics with sports, arts, community service, and "
            "environmental stewardship.</p>"
            "<p>With a student-teacher ratio of 20:1, personalised mentoring, and a "
            "culture that celebrates every child's unique potential, Green Valley has "
            "consistently produced outstanding academic results alongside well-rounded "
            "individuals.</p>"
        )
        a.image = "placeholder/about_campus_garden.jpg"
        a.established_year = 1998
        a.students_count = "1,850+"
        a.teachers_count = "95+"
        a.save()
        self.stdout.write('  ✓ Home About Section')

    # ─────────────────────────────────────────────────────────────
    #  4. VISION & MISSION (Singleton pk=1)
    # ─────────────────────────────────────────────────────────────
    def seed_vision_mission(self):
        vm, _ = VisionMission.objects.get_or_create(pk=1)
        vm.vision_title = "Our Vision"
        vm.vision_content = (
            "To be a centre of educational excellence rooted in Indian values, "
            "nurturing globally competent, socially responsible, and environmentally "
            "conscious citizens who lead with empathy, integrity, and innovation."
        )
        vm.mission_title = "Our Mission"
        vm.mission_content = (
            "To deliver a student-centred, inquiry-based education that:\n"
            "• Fosters intellectual curiosity and critical thinking\n"
            "• Develops strong moral character and emotional intelligence\n"
            "• Promotes physical fitness and mental well-being\n"
            "• Celebrates cultural diversity and inclusivity\n"
            "• Integrates technology meaningfully into learning\n"
            "• Instills a deep respect for nature and sustainable living"
        )
        vm.values_title = "Core Values"
        vm.values_content = (
            "Integrity — We uphold honesty and transparency in all we do.\n"
            "Excellence — We strive for the highest standards in academics and character.\n"
            "Respect — We honour every individual's dignity and perspective.\n"
            "Compassion — We cultivate kindness and empathy in our community.\n"
            "Innovation — We embrace creative thinking and continuous improvement.\n"
            "Sustainability — We act as responsible stewards of the environment.\n"
            "Collaboration — We believe in the power of teamwork and shared purpose."
        )
        vm.save()
        self.stdout.write('  ✓ Vision & Mission')

    # ─────────────────────────────────────────────────────────────
    #  5. PRINCIPAL MESSAGE (Singleton pk=1)
    # ─────────────────────────────────────────────────────────────
    def seed_principal_message(self):
        pm, _ = PrincipalMessage.objects.get_or_create(pk=1)
        pm.name = "Dr. Meera Krishnan"
        pm.title = "Principal"
        pm.qualification = "Ph.D. (Education), M.A. (English), B.Ed."
        pm.photo = "placeholder/principal_meera_krishnan.jpg"
        pm.message = (
            "Dear Parents and Students,\n\n"
            "Welcome to Green Valley Public School — a place where learning is a joyful "
            "journey and every child is cherished.\n\n"
            "At Green Valley, we believe that true education extends far beyond textbooks. "
            "Our classrooms are spaces of inquiry, our playgrounds are arenas of character, "
            "and our community is a family bound by shared values.\n\n"
            "Kerala has a long and proud tradition of prioritising education, and we are "
            "honoured to carry that legacy forward. Our dedicated faculty — many of whom "
            "have been with us for over a decade — work tirelessly to ensure that each "
            "student receives individual attention and is encouraged to explore their "
            "passions.\n\n"
            "As we embrace the challenges of a rapidly changing world, we remain committed "
            "to blending time-tested pedagogical practices with modern technology and "
            "21st-century skills. From our STEM labs to our Kalaripayattu sessions, from "
            "our model United Nations to our organic garden — we offer a rich tapestry of "
            "experiences that shape confident, compassionate leaders.\n\n"
            "I invite you to visit our campus, meet our team, and discover what makes "
            "Green Valley truly special.\n\n"
            "Warm regards,\n"
            "Dr. Meera Krishnan\n"
            "Principal, Green Valley Public School"
        )
        pm.save()
        self.stdout.write('  ✓ Principal Message')

    # ─────────────────────────────────────────────────────────────
    #  6. ABOUT PAGE (Singleton pk=1)
    # ─────────────────────────────────────────────────────────────
    def seed_about_page(self):
        ap, _ = AboutPage.objects.get_or_create(pk=1)
        ap.hero_title = "About Green Valley Public School"
        ap.hero_subtitle = (
            "Discover our story — from a humble beginning in 1998 to becoming one of "
            "Kottayam's most respected CBSE schools."
        )
        ap.history_title = "Our Journey"
        ap.history_content = (
            "<p>Green Valley Public School was founded in 1998 by the visionary "
            "educationist Sri. K. P. Varghese and a group of like-minded community "
            "leaders who dreamed of a school that would combine academic rigour with "
            "the warmth of Kerala's cultural ethos.</p>"
            "<p>Starting with just 120 students and 12 teachers in a rented building "
            "near Perumala Junction, the school earned its CBSE affiliation in 2002 "
            "and moved to its present 8-acre campus the same year. Over the following "
            "decades, Green Valley has grown steadily — adding new academic blocks, "
            "laboratories, sports facilities, and a performing-arts auditorium — while "
            "staying true to its founding principle: every child matters.</p>"
            "<p>Today, with nearly 1,850 students, 95 faculty members, and a vibrant "
            "alumni network spanning the globe, Green Valley Public School stands as a "
            "beacon of holistic education in central Kerala.</p>"
        )
        ap.history_image = "placeholder/about_history_1998.jpg"
        ap.infrastructure_title = "Our Campus & Infrastructure"
        ap.infrastructure_content = (
            "<p>Spread across 8 lush acres in the foothills of the Western Ghats, "
            "our eco-friendly campus features landscaped gardens, rain-water harvesting "
            "systems, and solar panels that meet 40% of our energy needs.</p>"
            "<p>The campus includes three academic blocks, a dedicated STEM wing, "
            "a 600-seat air-conditioned auditorium, an Olympic-size swimming pool, "
            "multi-sport courts, and a central library with over 25,000 volumes.</p>"
        )
        ap.save()
        self.stdout.write('  ✓ About Page')

    # ─────────────────────────────────────────────────────────────
    #  7. CONTACT PAGE (Singleton pk=1)
    # ─────────────────────────────────────────────────────────────
    def seed_contact_page(self):
        cp, _ = ContactPage.objects.get_or_create(pk=1)
        cp.hero_title = "Get in Touch"
        cp.hero_subtitle = (
            "We would love to hear from you. Whether you have a question about "
            "admissions, academics, or just want to say hello — our doors are always open."
        )
        cp.map_embed_code = (
            '<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3933.'
            '5!2d76.5222!3d9.5916!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s'
            '0x0%3A0x0!2z0LrQvtGC0YLQsNC50LDQvA!5e0!3m2!1sen!2sin!4v1'
            '!5m2!1sen!2sin" width="100%" height="450" style="border:0;" '
            'allowfullscreen="" loading="lazy" '
            'referrerpolicy="no-referrer-when-downgrade"></iframe>'
        )
        cp.save()
        self.stdout.write('  ✓ Contact Page')

    # ─────────────────────────────────────────────────────────────
    #  8. ACADEMICS PAGE (Singleton pk=1)
    # ─────────────────────────────────────────────────────────────
    def seed_academics_page(self):
        ap, _ = AcademicsPage.objects.get_or_create(pk=1)
        ap.hero_title = "Academics at Green Valley"
        ap.hero_subtitle = (
            "A rigorous, well-rounded CBSE curriculum designed to ignite curiosity "
            "and prepare students for the challenges of a dynamic world."
        )
        ap.hero_image = "placeholder/academics_hero_classroom.jpg"

        ap.overview_title = "Academic Excellence"
        ap.overview_content = (
            "<p>Green Valley Public School follows the CBSE curriculum enriched with "
            "experiential learning modules, STEM integration, and value-based education. "
            "Our academic programme spans Pre-Primary through Grade XII, with specialised "
            "streams in Science, Commerce, and Humanities at the senior-secondary level.</p>"
            "<p>We maintain a student-teacher ratio of 20:1 to ensure personalised "
            "attention. Continuous assessments, project-based learning, and regular "
            "parent-teacher consultations form the backbone of our evaluation philosophy.</p>"
        )

        ap.curriculum_title = "Our Curriculum"
        ap.curriculum_content = (
            "<p>Aligned with the CBSE framework and enriched by NEP 2020 guidelines, "
            "our curriculum integrates:</p>"
            "<ul>"
            "<li><strong>Foundational Literacy & Numeracy</strong> — Play-based learning "
            "in Pre-Primary and Grades I–II</li>"
            "<li><strong>Preparatory Stage</strong> — Structured subject introduction in "
            "Grades III–V with hands-on science and environmental studies</li>"
            "<li><strong>Middle Stage</strong> — Deep subject exploration, coding, and "
            "second-language proficiency in Grades VI–VIII</li>"
            "<li><strong>Secondary & Senior Secondary</strong> — Board-level rigour with "
            "electives, vocational courses, and competitive-exam coaching in Grades IX–XII</li>"
            "</ul>"
        )
        ap.curriculum_image = "placeholder/academics_curriculum_infographic.jpg"

        ap.methodology_title = "Our Teaching Methodology"
        ap.methodology_content = (
            "<p>We employ a blended pedagogical approach that combines:</p>"
            "<ul>"
            "<li><strong>Inquiry-Based Learning</strong> — Students explore, question, "
            "and discover concepts through guided investigation.</li>"
            "<li><strong>Flipped Classroom</strong> — Pre-class video lessons allow "
            "in-class time for discussion, problem-solving, and collaboration.</li>"
            "<li><strong>Project-Based Learning</strong> — Cross-curricular projects "
            "develop research, teamwork, and presentation skills.</li>"
            "<li><strong>Technology-Enhanced Instruction</strong> — Smart boards, "
            "learning management systems, and virtual labs bring lessons to life.</li>"
            "<li><strong>Differentiated Instruction</strong> — Activities are tailored "
            "to diverse learning styles and paces.</li>"
            "</ul>"
        )

        ap.calendar_title = "Academic Calendar 2026-27"
        ap.save()
        self.stdout.write('  ✓ Academics Page')

    # ─────────────────────────────────────────────────────────────
    #  9. ADMISSION SETTINGS (Singleton pk=1)
    # ─────────────────────────────────────────────────────────────
    def seed_admission_settings(self):
        s, _ = AdmissionSettings.objects.get_or_create(pk=1)
        s.is_open = True
        s.hero_title = "Admissions 2026-27"
        s.hero_subtitle = (
            "Join the Green Valley family! Applications are now open for "
            "Pre-Primary through Grade XI for the academic year 2026-27."
        )
        s.hero_image = "placeholder/admissions_hero_students.jpg"

        s.overview_title = "Admission Process"
        s.overview_content = (
            "<p>At Green Valley Public School, we follow a transparent and merit-based "
            "admission process. We welcome students from all backgrounds and believe "
            "every child deserves access to quality education.</p>"
            "<p>Admissions are granted on the basis of age-appropriateness, an informal "
            "interaction (for Pre-Primary and Grade I), or an entrance assessment "
            "(for Grades II and above), followed by a parent-student interview.</p>"
        )

        s.eligibility_title = "Eligibility & Age Criteria"
        s.eligibility_content = (
            "<p><strong>Pre-Primary (LKG):</strong> Child must be 3 years 6 months as on "
            "1st April of the admission year.</p>"
            "<p><strong>Pre-Primary (UKG):</strong> Child must be 4 years 6 months as on "
            "1st April of the admission year.</p>"
            "<p><strong>Grade I:</strong> Child must be 5 years 6 months as on "
            "1st April of the admission year.</p>"
            "<p><strong>Grades II – VIII:</strong> Transfer Certificate from the previous "
            "school and satisfactory performance in the entrance assessment.</p>"
            "<p><strong>Grade IX:</strong> Must have passed Grade VIII from a recognised "
            "school.</p>"
            "<p><strong>Grade XI:</strong> Minimum 60% aggregate in Grade X CBSE Board "
            "examinations. Stream-specific cut-offs may apply.</p>"
        )

        s.documents_required = (
            "Completed Application Form\n"
            "Birth Certificate (original + photocopy)\n"
            "Transfer Certificate / School Leaving Certificate from previous school\n"
            "Report Card / Mark Sheet of last two academic years\n"
            "Aadhaar Card of the student (photocopy)\n"
            "Aadhaar Card of both parents (photocopies)\n"
            "4 recent passport-size photographs of the student\n"
            "Address Proof (Ration Card / Utility Bill / Rental Agreement)\n"
            "Caste / Community Certificate (if applicable)\n"
            "Medical Fitness Certificate from a registered practitioner"
        )

        s.contact_info = (
            "Admissions Office, Green Valley Public School\n"
            "Mangalam Road, Perumala Junction, Kottayam — 686 561\n\n"
            "Email: admissions@greenvalleyschool.edu.in\n"
            "Phone: +91 481 253 4003\n"
            "WhatsApp: +91 94470 12346\n"
            "Office Hours: Mon – Fri, 9:00 AM – 3:30 PM | Sat, 9:00 AM – 12:00 PM"
        )
        s.application_form_link = "https://greenvalleyschool.edu.in/apply"
        s.save()
        self.stdout.write('  ✓ Admission Settings')

    # ─────────────────────────────────────────────────────────────
    #  10. QUICK LINKS
    # ─────────────────────────────────────────────────────────────
    def seed_quick_links(self):
        QuickLink.objects.all().delete()
        links = [
            ("About Us", "/about", 1, False),
            ("Admissions", "/admissions", 2, False),
            ("Academics", "/academics", 3, False),
            ("Facilities", "/facilities", 4, False),
            ("Gallery", "/gallery", 5, False),
            ("Events & News", "/events", 6, False),
            ("Notices", "/notices", 7, False),
            ("Contact Us", "/contact", 8, False),
            ("CBSE Portal", "https://www.cbse.gov.in", 9, True),
            ("Parent Login", "https://greenvalleyschool.edu.in/parent-portal", 10, True),
        ]
        for title, url, order, new_tab in links:
            QuickLink.objects.create(
                title=title, url=url, order=order,
                is_active=True, open_in_new_tab=new_tab
            )
        self.stdout.write('  ✓ Quick Links (10)')

    # ─────────────────────────────────────────────────────────────
    #  11. ACADEMIC HIGHLIGHTS
    # ─────────────────────────────────────────────────────────────
    def seed_academic_highlights(self):
        AcademicHighlight.objects.all().delete()
        highlights = [
            ("Board Pass Rate", "99.6%", "🎓", 1),
            ("Distinction Rate", "82%", "⭐", 2),
            ("Board Toppers", "38+", "🏆", 3),
            ("Faculty Members", "95+", "👩‍🏫", 4),
            ("Years of Excellence", "28", "📅", 5),
            ("Students Enrolled", "1,850+", "👨‍🎓", 6),
        ]
        for title, value, icon, order in highlights:
            AcademicHighlight.objects.create(
                title=title, value=value, icon=icon,
                order=order, is_active=True
            )
        self.stdout.write('  ✓ Academic Highlights (6)')

    # ─────────────────────────────────────────────────────────────
    #  12. CLASS CATEGORIES & SUBJECTS
    # ─────────────────────────────────────────────────────────────
    def seed_class_categories_and_subjects(self):
        Subject.objects.all().delete()
        ClassCategory.objects.all().delete()

        categories_data = [
            {
                "name": "Pre-Primary (LKG – UKG)",
                "description": (
                    "A play-based, activity-oriented programme designed to develop "
                    "foundational literacy, numeracy, motor skills, and social-emotional "
                    "readiness in a safe, joyful environment."
                ),
                "classes_range": "LKG – UKG",
                "order": 1,
                "subjects": [
                    ("English", "📖", True),
                    ("Malayalam", "📝", True),
                    ("Numeracy", "🔢", True),
                    ("Environmental Awareness", "🌿", True),
                    ("Art & Craft", "🎨", False),
                    ("Music & Movement", "🎵", False),
                ],
            },
            {
                "name": "Primary (Grades I – V)",
                "description": (
                    "Building a strong academic foundation through structured learning, "
                    "hands-on activities, and an integrated approach to language, "
                    "mathematics, science, and social awareness."
                ),
                "classes_range": "I – V",
                "order": 2,
                "subjects": [
                    ("English", "📖", True),
                    ("Malayalam", "📝", True),
                    ("Hindi", "📝", True),
                    ("Mathematics", "📐", True),
                    ("Environmental Studies (EVS)", "🌍", True),
                    ("General Knowledge", "💡", False),
                    ("Computer Science", "💻", False),
                    ("Art Education", "🎨", False),
                    ("Physical Education", "🏃", False),
                ],
            },
            {
                "name": "Middle School (Grades VI – VIII)",
                "description": (
                    "Deepening subject knowledge, encouraging analytical thinking, "
                    "and introducing students to specialised disciplines and coding."
                ),
                "classes_range": "VI – VIII",
                "order": 3,
                "subjects": [
                    ("English", "📖", True),
                    ("Malayalam", "📝", True),
                    ("Hindi / Sanskrit", "📝", True),
                    ("Mathematics", "📐", True),
                    ("Science", "🔬", True),
                    ("Social Science", "🌐", True),
                    ("Computer Science", "💻", False),
                    ("Art Education", "🎨", False),
                    ("Physical Education", "🏃", False),
                    ("Work Education", "🛠️", False),
                ],
            },
            {
                "name": "Secondary (Grades IX – X)",
                "description": (
                    "Rigorous CBSE board preparation with a focus on conceptual clarity, "
                    "practical work, and competitive-exam foundations."
                ),
                "classes_range": "IX – X",
                "order": 4,
                "subjects": [
                    ("English Language & Literature", "📖", True),
                    ("Malayalam / Hindi", "📝", True),
                    ("Mathematics (Standard / Basic)", "📐", True),
                    ("Science", "🔬", True),
                    ("Social Science", "🌐", True),
                    ("Information Technology", "💻", False),
                    ("Art Education", "🎨", False),
                    ("Physical Education & Health", "🏃", False),
                ],
            },
            {
                "name": "Senior Secondary – Science (Grades XI – XII)",
                "description": (
                    "An intensive science stream with optional Biology or Computer Science, "
                    "preparing students for engineering, medicine, and pure sciences."
                ),
                "classes_range": "XI – XII",
                "order": 5,
                "subjects": [
                    ("English Core", "📖", True),
                    ("Physics", "⚛️", True),
                    ("Chemistry", "🧪", True),
                    ("Mathematics", "📐", True),
                    ("Biology", "🧬", False),
                    ("Computer Science (Python)", "💻", False),
                    ("Physical Education", "🏃", False),
                ],
            },
            {
                "name": "Senior Secondary – Commerce (Grades XI – XII)",
                "description": (
                    "A comprehensive commerce stream equipping students for careers in "
                    "business, finance, chartered accountancy, and management."
                ),
                "classes_range": "XI – XII",
                "order": 6,
                "subjects": [
                    ("English Core", "📖", True),
                    ("Accountancy", "📊", True),
                    ("Business Studies", "💼", True),
                    ("Economics", "📈", True),
                    ("Mathematics / Informatics Practices", "📐", False),
                    ("Physical Education", "🏃", False),
                ],
            },
        ]

        for cat_data in categories_data:
            cat = ClassCategory.objects.create(
                name=cat_data["name"],
                description=cat_data["description"],
                classes_range=cat_data.get("classes_range", ""),
                image="placeholder/academics_category.jpg",
                order=cat_data["order"],
                is_active=True,
            )
            for sub_name, icon, is_core in cat_data["subjects"]:
                sub, _ = Subject.objects.get_or_create(
                    name=sub_name,
                    defaults={"icon": icon, "is_core": is_core, "is_active": True}
                )
                sub.categories.add(cat)

        self.stdout.write('  ✓ Class Categories (6) & Subjects')

    # ─────────────────────────────────────────────────────────────
    #  13. ADMISSION STEPS
    # ─────────────────────────────────────────────────────────────
    def seed_admission_steps(self):
        AdmissionStep.objects.all().delete()
        steps = [
            ("Online Registration", "Visit our website and fill in the online application form with your child's details, preferred grade, and parent information.", "📝", 1),
            ("Application Fee Payment", "Pay the non-refundable application processing fee of ₹500 online or at the school office.", "💳", 2),
            ("Document Submission", "Upload scanned copies of all required documents through the portal or submit them at the Admissions Office.", "📁", 3),
            ("Entrance Assessment", "Students applying for Grades II and above appear for an age-appropriate written assessment in English, Mathematics, and General Awareness.", "📝", 4),
            ("Parent–Student Interaction", "A brief interaction with the school's admission panel to understand the family's educational philosophy and the child's interests.", "🤝", 5),
            ("Admission Confirmation", "Shortlisted families receive an offer letter. Confirm the seat by completing fee payment within 10 working days.", "✅", 6),
        ]
        for title, desc, icon, order in steps:
            AdmissionStep.objects.create(
                title=title, description=desc, icon=icon, order=order
            )
        self.stdout.write('  ✓ Admission Steps (6)')

    # ─────────────────────────────────────────────────────────────
    #  14. TIMELINE EVENTS
    # ─────────────────────────────────────────────────────────────
    def seed_timeline_events(self):
        TimelineEvent.objects.all().delete()
        events = [
            ("1998", "Foundation", "Green Valley Public School was founded by Sri. K. P. Varghese and the Green Valley Educational Trust with 120 students and 12 passionate teachers in a rented building near Perumala Junction.", "placeholder/timeline_1998_foundation.jpg", 1),
            ("2002", "CBSE Affiliation & New Campus", "The school received CBSE affiliation (No. 930456) and relocated to its present 8-acre campus on Mangalam Road, complete with a new academic block and playground.", "placeholder/timeline_2002_campus.jpg", 2),
            ("2006", "First Board Batch", "The inaugural batch of 45 students appeared for CBSE Grade X examinations, achieving a 100% pass rate with 12 distinctions.", "placeholder/timeline_2006_results.jpg", 3),
            ("2010", "Senior Secondary Wing", "Grades XI – XII were launched with Science and Commerce streams, inaugurated by the District Collector.", "placeholder/timeline_2010_senior.jpg", 4),
            ("2014", "Digital Classrooms", "All classrooms were upgraded with interactive smart boards, projectors, and high-speed Wi-Fi as part of the Digital India initiative.", "placeholder/timeline_2014_digital.jpg", 5),
            ("2017", "Sports Complex & Swimming Pool", "A multi-sport complex and Olympic-size swimming pool were inaugurated, establishing Green Valley as a hub for athletics in the district.", "placeholder/timeline_2017_sports.jpg", 6),
            ("2019", "STEM Innovation Centre", "The state-of-the-art STEM Innovation Centre was opened, featuring robotics, AI, and IoT labs, funded by the school trust and an ATAL Innovation Mission grant.", "placeholder/timeline_2019_stem.jpg", 7),
            ("2022", "Green Campus Certification", "Received the prestigious Green Campus certification from the Kerala State Pollution Control Board for solar energy, rainwater harvesting, and waste management initiatives.", "placeholder/timeline_2022_green.jpg", 8),
            ("2025", "Silver Jubilee & Auditorium", "Celebrated 25+ years of excellence with the inauguration of the 600-seat Varghese Memorial Auditorium and a vibrant alumni reunion.", "placeholder/timeline_2025_jubilee.jpg", 9),
        ]
        for year, title, desc, img, order in events:
            TimelineEvent.objects.create(
                year=year, title=title, description=desc,
                image=img, order=order
            )
        self.stdout.write('  ✓ Timeline Events (9)')

    # ─────────────────────────────────────────────────────────────
    #  15. MANAGEMENT MEMBERS
    # ─────────────────────────────────────────────────────────────
    def seed_management_members(self):
        ManagementMember.objects.all().delete()
        members = [
            {
                "name": "Sri. K. P. Varghese",
                "position": "Founder & Chairman",
                "bio": "A retired IAS officer and visionary educationist, Sri. Varghese established the Green Valley Educational Trust in 1997 with the aim of making quality education accessible to every child in central Kerala. Under his stewardship, the school has grown from a single building to an 8-acre campus.",
                "email": "chairman@greenvalleyschool.edu.in",
                "phone": "+91 94470 10001",
                "order": 1,
            },
            {
                "name": "Smt. Lakshmi Varghese",
                "position": "Vice Chairperson",
                "bio": "An alumna of Women's Christian College, Chennai, Smt. Lakshmi oversees academic policy, scholarship programmes, and community outreach. She has been instrumental in introducing the school's environmental sustainability initiatives.",
                "email": "vicechairperson@greenvalleyschool.edu.in",
                "phone": "+91 94470 10002",
                "order": 2,
            },
            {
                "name": "Dr. Meera Krishnan",
                "position": "Principal",
                "bio": "With over 22 years of experience in education and a Ph.D. in Curriculum Design, Dr. Krishnan leads the academic and administrative functions of the school. She is a published researcher and a regular speaker at national education conferences.",
                "email": "principal@greenvalleyschool.edu.in",
                "phone": "+91 94470 10003",
                "order": 3,
            },
            {
                "name": "Mr. Thomas Mathew",
                "position": "Vice Principal (Academics)",
                "bio": "An M.Sc. in Physics with 18 years of teaching experience, Mr. Mathew coordinates the academic programme across all grades and mentors the faculty professional development initiative.",
                "email": "vp.academics@greenvalleyschool.edu.in",
                "phone": "+91 94470 10004",
                "order": 4,
            },
            {
                "name": "Mrs. Anjali Nair",
                "position": "Vice Principal (Administration)",
                "bio": "An MBA in Education Management, Mrs. Nair manages school operations, infrastructure, transport, and non-teaching staff. She is the architect of the school's digital transformation roadmap.",
                "email": "vp.admin@greenvalleyschool.edu.in",
                "phone": "+91 94470 10005",
                "order": 5,
            },
            {
                "name": "Mr. Rajesh Menon",
                "position": "Secretary, School Trust",
                "bio": "A practising chartered accountant, Mr. Menon manages the trust's finances, audits, and regulatory compliance. He also chairs the school's scholarship committee.",
                "email": "secretary@greenvalleyschool.edu.in",
                "phone": "+91 94470 10006",
                "order": 6,
            },
        ]
        for m in members:
            ManagementMember.objects.create(
                photo="placeholder/management_member.jpg",
                is_active=True,
                **m
            )
        self.stdout.write('  ✓ Management Members (6)')

    # ─────────────────────────────────────────────────────────────
    #  16. FACILITIES
    # ─────────────────────────────────────────────────────────────
    def seed_facilities(self):
        Facility.objects.all().delete()
        facilities = [
            {
                "name": "Smart Classrooms",
                "short_description": "65 air-conditioned, sound-insulated classrooms equipped with 75-inch interactive flat panels, surround-sound speakers, and high-speed Wi-Fi for an immersive digital learning experience.",
                "long_description": "<p>Our smart classrooms are designed with ergonomic furniture, anti-glare LED lighting, and green boards in addition to the interactive flat panels. Each room is connected to the school's learning management system, allowing teachers to share multimedia content, conduct live quizzes, and record lessons for revision.</p><p>Classrooms for lower grades feature play corners and reading nooks, while senior-secondary rooms include discussion pods for group projects.</p>",
                "icon": "💻",
                "gallery_captions": ["Interactive panel demo", "Ergonomic seating arrangement", "Grade III classroom activity"],
            },
            {
                "name": "Science Laboratories",
                "short_description": "Dedicated Physics, Chemistry, Biology, and Composite Science labs with modern apparatus, fume hoods, and digital microscopes for rigorous practical learning.",
                "long_description": "<p>The school houses four specialised science laboratories — Physics, Chemistry, Biology, and a Composite Science lab for middle-school students. Each lab accommodates 40 students and is outfitted with explosion-proof fume cupboards, electronic balances, digital data-logging equipment, and projector-linked demonstration benches.</p><p>The Biology lab features a botanical specimen collection and a 3D anatomy model set.</p>",
                "icon": "🔬",
                "gallery_captions": ["Physics lab bench setup", "Chemistry fume hood", "Students performing titration"],
            },
            {
                "name": "STEM Innovation Centre",
                "short_description": "A cutting-edge facility with robotics, artificial intelligence, IoT, and 3D-printing stations — where students turn ideas into prototypes.",
                "long_description": "<p>Launched in 2019 with support from ATAL Innovation Mission, the STEM Centre is a 3,000 sq. ft. maker-space featuring Arduino and Raspberry Pi kits, 3D printers, laser cutters, drone assembly stations, and an AI workstation with GPU support.</p><p>Students from Grade V upwards participate in weekly STEM hours, and the centre has hosted three district-level hackathons.</p>",
                "icon": "🤖",
                "gallery_captions": ["Robotics workstation", "3D printer in action", "IoT project showcase"],
            },
            {
                "name": "Computer Labs",
                "short_description": "Two fully networked computer labs with 80 workstations running the latest software, plus a dedicated coding lab for competitive programming.",
                "long_description": "<p>Lab 1 serves general IT literacy with licensed office suites and creative software. Lab 2 — the Coding Lab — is configured for Python, Java, and web development, with each workstation connected to GitHub and cloud IDEs.</p><p>Both labs have UPS backup and 100 Mbps fibre-optic connectivity.</p>",
                "icon": "🖥️",
                "gallery_captions": ["Main computer lab", "Coding lab workstations"],
            },
            {
                "name": "Library & Media Centre",
                "short_description": "A two-storey central library housing 25,000+ books, e-books, journals, and an AV room, fostering a lifelong love for reading and research.",
                "long_description": "<p>The Varghese Memorial Library spans 5,000 sq. ft. across two floors. The ground floor houses the primary section, periodicals, and a storytelling corner. The upper floor features the reference section, competitive-exam resources, a silent reading zone, and a 30-seat audio-visual room with surround sound.</p><p>Students access the digital catalogue via OPAC terminals and the school app.</p>",
                "icon": "📚",
                "gallery_captions": ["Library reading hall", "Primary section storytelling corner", "Digital catalogue terminal"],
            },
            {
                "name": "Sports Complex & Swimming Pool",
                "short_description": "Multi-sport facilities including an Olympic-size pool, 400m athletics track, cricket pitch, football field, basketball and tennis courts, and an indoor badminton hall.",
                "long_description": "<p>The sports complex covers 3 acres and features a FINA-standard 50m swimming pool with heated lanes, a synthetic 400m athletics track, a turf cricket pitch with practice nets, a FIFA-dimension football field, two basketball courts, two tennis courts (hard court), and an indoor badminton hall.</p><p>Full-time coaches for swimming, cricket, football, basketball, athletics, and badminton train students throughout the year. The school has produced 12 state-level athletes in the past five years.</p>",
                "icon": "🏊",
                "gallery_captions": ["Olympic-size swimming pool", "Athletics track", "Indoor badminton court"],
            },
            {
                "name": "Performing Arts Auditorium",
                "short_description": "A 600-seat, fully air-conditioned auditorium with professional lighting, a Dolby sound system, and a motorised stage for assemblies, performances, and conferences.",
                "long_description": "<p>The Varghese Memorial Auditorium, inaugurated in 2025, features tiered seating, a 40 ft. motorised proscenium stage, green rooms, a Dolby Atmos sound system, and intelligent LED stage lighting. It hosts the school's daily assembly, annual day, inter-school cultural festivals, and community events.</p>",
                "icon": "🎭",
                "gallery_captions": ["Auditorium interior", "Stage during annual day", "Sound & lighting console"],
            },
            {
                "name": "Cafeteria & Dining Hall",
                "short_description": "A spacious, FSSAI-certified cafeteria serving nutritious vegetarian and non-vegetarian meals, fresh juices, and snacks in a hygienic environment.",
                "long_description": "<p>The 200-seat dining hall operates a buffet-style lunch service prepared by trained kitchen staff under FSSAI guidelines. The menu rotates weekly and includes traditional Kerala cuisine alongside North Indian and Continental options. A salad bar and fresh-fruit counter are available daily. Special dietary needs — including allergies — are accommodated upon request.</p>",
                "icon": "🍽️",
                "gallery_captions": ["Dining hall interior", "Kitchen food preparation", "Salad and fruit bar"],
            },
            {
                "name": "Transport Services",
                "short_description": "A fleet of 18 GPS-tracked, CCTV-equipped school buses covering 25+ routes across Kottayam and neighbouring districts.",
                "long_description": "<p>Safety is our priority. Each bus is equipped with GPS tracking (accessible to parents via the school app), CCTV cameras, a speed governor, a fire extinguisher, and a first-aid kit. Trained drivers and female attendants accompany every trip. Routes cover Kottayam town, Pala, Changanassery, Ettumanoor, Erattupetta, and surrounding areas.</p>",
                "icon": "🚌",
                "gallery_captions": ["School bus fleet", "GPS tracking dashboard"],
            },
            {
                "name": "Health & Wellness Centre",
                "short_description": "An on-campus medical room staffed by a qualified nurse and a visiting paediatrician, with a school counsellor available for mental-health support.",
                "long_description": "<p>The Health Centre is equipped with an examination bed, basic diagnostic instruments, an emergency oxygen cylinder, and a stock of essential medications. A qualified nurse is on duty throughout school hours, and a paediatrician visits twice a week. The centre maintains individual health records for every student.</p><p>A full-time certified school counsellor provides emotional and behavioural support, conducts resilience workshops, and runs peer-mediation programmes.</p>",
                "icon": "🏥",
                "gallery_captions": ["Medical room", "Counselling room"],
            },
        ]

        for i, f in enumerate(facilities):
            fac = Facility.objects.create(
                name=f["name"],
                short_description=f["short_description"],
                long_description=f.get("long_description", ""),
                icon=f["icon"],
                cover_image="placeholder/facility_cover.jpg",
                order=i,
                is_active=True,
            )
            for j, caption in enumerate(f.get("gallery_captions", [])):
                FacilityImage.objects.create(
                    facility=fac,
                    image="placeholder/facility_gallery.jpg",
                    caption=caption,
                    order=j,
                    is_active=True,
                )
        self.stdout.write(f'  ✓ Facilities ({len(facilities)}) & Gallery Images')

    # ─────────────────────────────────────────────────────────────
    #  17. ACHIEVEMENTS
    # ─────────────────────────────────────────────────────────────
    def seed_achievements(self):
        Achievement.objects.all().delete()
        achievements = [
            ("CBSE Grade XII — 99.6% Pass Rate", "Our Grade XII batch of 2025 achieved an exceptional 99.6% pass rate, with 42 students scoring above 90% aggregate and 3 students securing centum in Mathematics.", "2025", 1),
            ("CBSE Grade X — 100% Pass Rate", "All 165 students of the Grade X batch of 2025 cleared the board examinations. The school topper, Arjun S. Nair, scored 498/500.", "2025", 2),
            ("National Science Olympiad — 8 Qualifiers", "Eight students qualified for the national round of the Science Olympiad Foundation's NSO 2024, with two securing top-100 national ranks.", "2024", 3),
            ("State-Level Football Champions", "The U-17 boys' football team won the CBSE Kerala Cluster football championship, defeating 48 participating schools.", "2024", 4),
            ("INSPIRE Award – MANAK Scheme", "Six students were selected for the INSPIRE Award under the MANAK scheme by the Department of Science & Technology, Government of India.", "2024", 5),
            ("Green Campus Certification", "Awarded the Green Campus certification by the Kerala State Pollution Control Board for outstanding solar energy adoption, rainwater harvesting, and waste management.", "2022", 6),
            ("Best School Award – Kottayam District", "Recognised as the Best CBSE School in Kottayam District by the Kerala State Education Board for consistent academic excellence and co-curricular achievements.", "2023", 7),
            ("Inter-School Debate — State Winner", "Deepthi Menon of Grade XI won the first prize at the State-Level Inter-School Debate Competition organised by the Kerala Debate Association.", "2025", 8),
            ("National Robotics Championship — Finalists", "Team Green Bots (4 students from Grades IX–X) reached the national finals of the WRO India Robotics Championship held in Bengaluru.", "2024", 9),
            ("Swimming — State Gold Medals", "Adarsh Kurien (Grade IX) won 2 gold medals in 50m and 100m freestyle at the Kerala State Aquatic Meet.", "2025", 10),
        ]
        for title, desc, year, order in achievements:
            Achievement.objects.create(
                title=title, description=desc, year=year,
                image="placeholder/achievement.jpg",
                order=order, is_active=True
            )
        self.stdout.write(f'  ✓ Achievements ({len(achievements)})')

    # ─────────────────────────────────────────────────────────────
    #  18. TESTIMONIALS
    # ─────────────────────────────────────────────────────────────
    def seed_testimonials(self):
        Testimonial.objects.all().delete()
        testimonials = [
            ("Smt. Deepa Menon", "Parent (Grade VII & X)", "Green Valley has been a second home for both my children. The teachers genuinely care about every student's progress — academic and emotional. The personalised attention our children receive here is something we deeply value.", 5, 1),
            ("Arjun S. Nair", "Alumni — Batch of 2024", "I owe my success at IIT Madras to the solid foundation I received at Green Valley. The STEM lab, the dedicated Physics faculty, and the competitive-exam coaching programme gave me the edge I needed.", 5, 2),
            ("Mr. George Thomas", "Parent (Grade III)", "From the moment we walked onto the campus, we knew this was the right school for our daughter. The green environment, caring staff, and emphasis on experiential learning make Green Valley truly special.", 5, 3),
            ("Lakshmi Priya R.", "Alumni — Batch of 2022", "The values Green Valley instilled in me — empathy, perseverance, and a love for learning — continue to guide me in my medical studies at AIIMS Delhi. I'm proud to be a Green Valleyite!", 5, 4),
            ("Dr. Anoop Kumar", "Parent (Grade IX)", "As a doctor, I appreciate the school's focus on mental health and physical fitness. The counselling services, swimming coaching, and balanced academic pressure create a healthy learning environment.", 4, 5),
            ("Fathima Zahra", "Alumni — Batch of 2023", "The Model United Nations, debate club, and leadership programmes at Green Valley shaped my confidence and communication skills. I am now studying International Relations at JNU.", 5, 6),
            ("Mrs. Priya Suresh", "Parent (LKG & Grade IV)", "The pre-primary programme is wonderfully designed. My younger one looks forward to school every day! The transition from play-based learning to structured academics has been smooth and joyful.", 5, 7),
            ("Vishnu Nair", "Alumni — Batch of 2020", "Green Valley taught me to dream big. The school's emphasis on sports helped me earn a football scholarship to a university in the UK. Thank you, Green Valley!", 5, 8),
        ]
        for name, role, content, rating, order in testimonials:
            Testimonial.objects.create(
                name=name, role=role, content=content,
                rating=rating, order=order,
                photo="placeholder/testimonial_avatar.jpg",
                is_active=True
            )
        self.stdout.write(f'  ✓ Testimonials ({len(testimonials)})')

    # ─────────────────────────────────────────────────────────────
    #  19. NOTICES
    # ─────────────────────────────────────────────────────────────
    def seed_notices(self):
        Notice.objects.all().delete()
        today = timezone.now().date()
        notices = [
            {
                "title": "Admissions Open for 2026-27 Academic Year",
                "content": "<p>Green Valley Public School is pleased to announce that admissions for the academic year 2026-27 are now open for Pre-Primary through Grade XI.</p><p>Interested parents may collect application forms from the school office or apply online at <strong>greenvalleyschool.edu.in/apply</strong>. The last date for submission is 28 February 2026.</p><p>For queries, contact the Admissions Office at +91 481 253 4003 or email admissions@greenvalleyschool.edu.in.</p>",
                "is_important": True,
                "status": "published",
                "publish_date": today - timedelta(days=5),
                "expiry_date": today + timedelta(days=60),
            },
            {
                "title": "Onam Celebration – Cultural Programme Schedule",
                "content": "<p>The school will celebrate Onam on <strong>22 August 2026</strong> with a grand cultural programme. Students are encouraged to wear traditional Kerala attire (Kasavu Mundu / Onam Dress).</p><p><strong>Schedule:</strong></p><ul><li>8:30 AM – Pookalam competition (House-wise)</li><li>10:00 AM – Cultural programme (Thiruvathira, Pulikali, Onappattu)</li><li>12:00 PM – Onasadya (traditional feast) in the dining hall</li></ul><p>Parents are cordially invited to attend the cultural programme.</p>",
                "is_important": True,
                "status": "published",
                "publish_date": today - timedelta(days=2),
                "expiry_date": today + timedelta(days=45),
            },
            {
                "title": "Parent-Teacher Meeting – July 2026",
                "content": "<p>The Parent-Teacher Meeting for Grades I to X is scheduled as follows:</p><ul><li><strong>Grades I – V:</strong> Saturday, 18 July 2026, 9:00 AM – 12:00 PM</li><li><strong>Grades VI – X:</strong> Saturday, 25 July 2026, 9:00 AM – 12:00 PM</li></ul><p>Parents are requested to carry the student diary and previous assessment reports. Please arrive 15 minutes before the scheduled time.</p>",
                "is_important": False,
                "status": "published",
                "publish_date": today - timedelta(days=10),
                "expiry_date": today + timedelta(days=20),
            },
            {
                "title": "Inter-House Sports Meet 2026 – Registration Open",
                "content": "<p>The Annual Inter-House Sports Meet will be held from <strong>5 to 7 August 2026</strong> at the school sports complex.</p><p>Events include track & field, swimming, football (5-a-side), basketball, and badminton. Students wishing to participate must register with their House Captains or Physical Education teachers by 20 July 2026.</p><p>Practice sessions begin from 14 July 2026 during the PE period and after school hours (3:45 – 5:00 PM).</p>",
                "is_important": False,
                "status": "published",
                "publish_date": today - timedelta(days=7),
                "expiry_date": today + timedelta(days=30),
            },
            {
                "title": "Annual Science Exhibition – Call for Projects",
                "content": "<p>The Annual Science Exhibition will be held on <strong>15 September 2026</strong>. Students from Grades VI to XII are invited to submit project proposals under the following themes:</p><ol><li>Sustainable Energy</li><li>AI & Machine Learning Applications</li><li>Waste Management Innovations</li><li>Space Exploration</li></ol><p>Project synopsis (max 500 words) must be submitted to the respective science teachers by 10 August 2026. Shortlisted teams will receive a ₹2,000 materials grant from the STEM Centre.</p>",
                "is_important": False,
                "status": "published",
                "publish_date": today - timedelta(days=3),
                "expiry_date": today + timedelta(days=70),
            },
            {
                "title": "School Closed — Independence Day",
                "content": "<p>The school will remain closed on <strong>15 August 2026 (Saturday)</strong> on account of Independence Day.</p><p>A flag-hoisting ceremony and cultural programme will be held in the school auditorium on <strong>14 August 2026 (Friday)</strong> from 8:30 AM. All students are expected to attend in full uniform.</p>",
                "is_important": False,
                "status": "published",
                "publish_date": today - timedelta(days=1),
                "expiry_date": today + timedelta(days=35),
            },
            {
                "title": "CBSE Circular — New Assessment Guidelines for 2026-27",
                "content": "<p>As per CBSE Circular No. Acad-42/2026 dated 01 July 2026, the following changes in the assessment pattern apply from the current academic year:</p><ul><li>Internal Assessment weightage increased to 30% for Grades IX and X.</li><li>Competency-based questions will constitute 40% of board papers.</li><li>Project work to include one cross-disciplinary project per term.</li></ul><p>Detailed guidelines will be shared by class teachers during the PTM.</p>",
                "is_important": True,
                "status": "published",
                "publish_date": today - timedelta(days=12),
                "expiry_date": today + timedelta(days=90),
            },
            {
                "title": "Bus Route Revision – Pala & Changanassery Routes",
                "content": "<p>Please note the revised timings for Bus Routes 7 (Pala) and 12 (Changanassery) effective from <strong>21 July 2026</strong>:</p><ul><li><strong>Route 7 (Pala):</strong> Departure from Pala Bus Stand at 7:15 AM (earlier: 7:30 AM)</li><li><strong>Route 12 (Changanassery):</strong> Departure from Changanassery Railway Station at 7:00 AM (earlier: 7:20 AM)</li></ul><p>Parents are requested to ensure students are at their designated stops 5 minutes before departure.</p>",
                "is_important": False,
                "status": "published",
                "publish_date": today - timedelta(days=8),
                "expiry_date": today + timedelta(days=30),
            },
        ]
        for n in notices:
            Notice.objects.create(**n, attachment=None)
        self.stdout.write(f'  ✓ Notices ({len(notices)})')

    # ─────────────────────────────────────────────────────────────
    #  20. EVENTS
    # ─────────────────────────────────────────────────────────────
    def seed_events(self):
        Event.objects.all().delete()
        today = timezone.now().date()
        events = [
            {
                "title": "Annual Day 2026 — 'Rhythm of the Valley'",
                "excerpt": "A spectacular evening of dance, drama, and music celebrating the creativity and talent of Green Valley students.",
                "content": "<p>The 27th Annual Day celebration, themed <strong>'Rhythm of the Valley'</strong>, will feature performances by students from Pre-Primary to Grade XII. Highlights include a Mohiniyattam ensemble, a rock-band performance by the school music club, a one-act play on environmental awareness, and the annual prize distribution.</p><p><strong>Date:</strong> 18 December 2026<br/><strong>Venue:</strong> Varghese Memorial Auditorium<br/><strong>Time:</strong> 5:00 PM onwards<br/><strong>Chief Guest:</strong> Padma Shri Dr. Leela Menon</p><p>Parents and alumni are warmly invited.</p>",
                "event_date": today + timedelta(days=158),
                "is_featured": True,
                "status": "published",
            },
            {
                "title": "Inter-House Sports Meet 2026",
                "excerpt": "Three days of thrilling athletic competition across four houses — Sahyadri, Periyar, Vembanad, and Nilgiri.",
                "content": "<p>The Annual Inter-House Sports Meet brings together students from Grades I to XII in a celebration of sportsmanship and fitness.</p><p><strong>Events:</strong> 100m, 200m, 400m, 800m, 4×100m relay, long jump, high jump, shot put, swimming (50m, 100m), football (5-a-side), basketball, and badminton.</p><p><strong>Dates:</strong> 5 – 7 August 2026<br/><strong>Venue:</strong> School Sports Complex<br/><strong>Inauguration:</strong> 5 Aug, 8:30 AM — Chief Guest: Mr. Anil Kumar, former Olympian</p>",
                "event_date": today + timedelta(days=23),
                "is_featured": True,
                "status": "published",
            },
            {
                "title": "Science Exhibition — 'Innovate for Tomorrow'",
                "excerpt": "Students present innovative science projects addressing real-world challenges in sustainability, AI, and health.",
                "content": "<p>The annual Science Exhibition invites students from Grades VI to XII to showcase projects under themes of Sustainable Energy, AI Applications, Waste Management, and Space Exploration.</p><p>An external panel of scientists from CSIR-NIIST and IISER Thiruvananthapuram will evaluate projects. The top 3 projects receive funding to represent the school at the CBSE National Science Exhibition.</p><p><strong>Date:</strong> 15 September 2026<br/><strong>Venue:</strong> STEM Innovation Centre & Main Corridor<br/><strong>Open to visitors:</strong> 10:00 AM – 3:00 PM</p>",
                "event_date": today + timedelta(days=64),
                "is_featured": True,
                "status": "published",
            },
            {
                "title": "Independence Day Celebration",
                "excerpt": "Flag hoisting, patriotic performances, and a special address by an Army officer mark India's 80th Independence Day at Green Valley.",
                "content": "<p>Join us for a solemn and uplifting Independence Day celebration featuring:</p><ul><li>Flag hoisting by the Chief Guest, Col. Suresh Babu (Retd.)</li><li>NCC cadets' march past</li><li>Patriotic songs and speeches by students</li><li>Quiz on Indian freedom fighters</li></ul><p><strong>Date:</strong> 14 August 2026 (Eve celebration)<br/><strong>Venue:</strong> School Main Ground<br/><strong>Time:</strong> 8:30 AM</p>",
                "event_date": today + timedelta(days=32),
                "is_featured": False,
                "status": "published",
            },
            {
                "title": "Onam Celebration 2026",
                "excerpt": "Experience the spirit of Kerala's harvest festival with Pookalam, Thiruvathira, Pulikali, and a grand Onasadya.",
                "content": "<p>Green Valley celebrates Onam with traditional grandeur! The day's programme includes:</p><ul><li>Pookalam (floral carpet) competition — House-wise</li><li>Thiruvathira dance and Pulikali performance</li><li>Onappattu (folk songs) by the music club</li><li>Traditional Onasadya served on banana leaves in the dining hall</li></ul><p><strong>Date:</strong> 22 August 2026<br/><strong>Venue:</strong> School Campus<br/><strong>Dress Code:</strong> Traditional Kerala attire</p>",
                "event_date": today + timedelta(days=40),
                "is_featured": False,
                "status": "published",
            },
            {
                "title": "Career Guidance Seminar — 'Pathways 2026'",
                "excerpt": "A half-day seminar for Grades X–XII students and parents featuring expert talks on engineering, medicine, law, design, and emerging careers.",
                "content": "<p>Green Valley's annual career guidance seminar, <strong>'Pathways'</strong>, brings together industry professionals and academic counsellors to help students and parents make informed decisions about higher education and careers.</p><p><strong>Speakers:</strong></p><ul><li>Prof. Ravi Shankar, IIT Bombay — Engineering & Technology</li><li>Dr. Nisha Mathew, AIIMS — Medical Sciences</li><li>Adv. Preethi Thomas — Law & Governance</li><li>Ms. Aisha Khan, NID — Design & Creative Arts</li></ul><p><strong>Date:</strong> 12 October 2026<br/><strong>Venue:</strong> Varghese Memorial Auditorium<br/><strong>Time:</strong> 9:00 AM – 1:00 PM</p>",
                "event_date": today + timedelta(days=91),
                "is_featured": False,
                "status": "published",
            },
            {
                "title": "Kerala Piravi Day — Cultural Programme",
                "excerpt": "Celebrating the formation of Kerala with literary readings, folk performances, and a tribute to Malayalam literature.",
                "content": "<p>On 1 November, Green Valley pays tribute to the rich heritage of Kerala with a special cultural programme:</p><ul><li>Recitation of poems by Changampuzha and Sugathakumari</li><li>Kathakali and Theyyam excerpts by the school drama club</li><li>Essay writing competition on 'Kerala — My Pride' for Grades VI – XII</li><li>Exhibition of traditional Kerala crafts by primary students</li></ul><p><strong>Date:</strong> 1 November 2026<br/><strong>Venue:</strong> Auditorium & Exhibition Hall<br/><strong>Time:</strong> 9:00 AM onwards</p>",
                "event_date": today + timedelta(days=111),
                "is_featured": False,
                "status": "published",
            },
        ]
        for e in events:
            Event.objects.create(
                image="placeholder/event_cover.jpg",
                **e
            )
        self.stdout.write(f'  ✓ Events ({len(events)})')

    # ─────────────────────────────────────────────────────────────
    #  21. GALLERY
    # ─────────────────────────────────────────────────────────────
    def seed_gallery(self):
        GalleryImage.objects.all().delete()
        GalleryCategory.objects.all().delete()
        categories = [
            {
                "name": "Campus & Infrastructure",
                "images": [
                    ("Aerial view of the 8-acre campus", True),
                    ("Academic Block A — front entrance", False),
                    ("Landscaped gardens and walkways", False),
                    ("Varghese Memorial Auditorium exterior", False),
                    ("Solar panel installation on Block B", False),
                ],
            },
            {
                "name": "Annual Day 2025",
                "images": [
                    ("Mohiniyattam dance performance", True),
                    ("School choir singing 'Vande Mataram'", False),
                    ("Prize distribution ceremony", False),
                    ("Students during the finale tableau", False),
                ],
            },
            {
                "name": "Sports & Athletics",
                "images": [
                    ("U-17 football team — district champions", True),
                    ("Swimming competition at the school pool", False),
                    ("Athletics track — 400m race", False),
                    ("Basketball inter-house finals", False),
                    ("Badminton tournament in the indoor hall", False),
                ],
            },
            {
                "name": "Science Fair 2025",
                "images": [
                    ("Winning project on solar water purification", True),
                    ("Robotics demonstration by Team Green Bots", False),
                    ("AI project on crop-disease detection", False),
                    ("Visitors viewing student exhibits", False),
                ],
            },
            {
                "name": "Cultural Events",
                "images": [
                    ("Onam celebration — Pookalam competition", True),
                    ("Thiruvathira dance during Onam", False),
                    ("Republic Day parade — NCC cadets", False),
                    ("Kerala Piravi — Kathakali performance", False),
                    ("Christmas carol singing by the choir", False),
                ],
            },
            {
                "name": "Classrooms & Labs",
                "images": [
                    ("Smart classroom — interactive panel lesson", True),
                    ("Chemistry lab — titration experiment", False),
                    ("STEM Centre — 3D printing session", False),
                    ("Library — silent reading zone", False),
                ],
            },
            {
                "name": "Community Service",
                "images": [
                    ("Tree planting drive at Perumala village", True),
                    ("Blood donation camp — NSS volunteers", False),
                    ("Flood relief material distribution (2024)", False),
                ],
            },
        ]
        for i, cat_data in enumerate(categories):
            cat = GalleryCategory.objects.create(name=cat_data["name"], order=i)
            for j, (caption, featured) in enumerate(cat_data["images"]):
                GalleryImage.objects.create(
                    category=cat,
                    title=caption,
                    caption=caption,
                    image="placeholder/gallery_image.jpg",
                    is_featured=featured,
                    order=j,
                )
        self.stdout.write(f'  ✓ Gallery Categories ({len(categories)}) & Images')

    # ─────────────────────────────────────────────────────────────
    #  22. DOCUMENTATION (Downloads)
    # ─────────────────────────────────────────────────────────────
    def seed_documentation(self):
        Documentation.objects.all().delete()
        docs = [
            ("Admission Application Form 2026-27", "Download and print the admission application form for the academic year 2026-27. Submit the completed form along with required documents at the school office.", 1),
            ("Fee Structure 2026-27", "Detailed fee structure for all grades from Pre-Primary to Grade XII for the academic year 2026-27, including tuition, transport, and activity fees.", 2),
            ("Academic Calendar 2026-27", "Month-by-month academic calendar with term dates, examination schedules, holidays, and important school events.", 3),
            ("School Prospectus 2026", "Comprehensive information about Green Valley Public School — history, vision, academics, facilities, co-curricular activities, and fee details.", 4),
            ("Holiday List 2026-27", "Complete list of public holidays, festival breaks, and vacation periods for the current academic year.", 5),
            ("Student Code of Conduct", "The school's code of conduct outlining expectations for student behaviour, uniform, attendance, and use of school property.", 6),
            ("CBSE Affiliation Certificate", "Copy of the school's current CBSE affiliation certificate (Affiliation No. 930456).", 7),
            ("Transfer Certificate Application Form", "Form for requesting a Transfer Certificate (TC) from the school. Submit at least 15 working days before the desired date.", 8),
            ("School Magazine — 'Green Echoes' 2025", "Digital copy of the annual school magazine featuring student writings, art, achievements, and faculty reflections.", 9),
            ("Anti-Bullying Policy", "Green Valley's comprehensive anti-bullying policy outlining prevention strategies, reporting procedures, and support mechanisms.", 10),
        ]
        for title, desc, order in docs:
            Documentation.objects.create(
                title=title, description=desc,
                order=order, is_active=True
            )
        self.stdout.write(f'  ✓ Documentation / Downloads ({len(docs)})')

    # ─────────────────────────────────────────────────────────────
    #  23. CONTACT SUBMISSIONS (sample)
    # ─────────────────────────────────────────────────────────────
    def seed_contact_submissions(self):
        ContactSubmission.objects.all().delete()
        submissions = [
            ("Anil Kumar", "anil.kumar@email.com", "+91 94470 56789", "Admission Inquiry for Grade V", "Dear Sir/Madam, I would like to inquire about the admission process and seat availability for my son in Grade V for the academic year 2026-27. Kindly share the details. Regards, Anil Kumar."),
            ("Reshma Suresh", "reshma.suresh@email.com", "+91 98470 34567", "Transport Route — Pala", "Hello, we are relocating to Pala and would like to know if there is a school bus route covering the Pala–Bharananganam stretch. My daughter is currently in Grade III. Thank you."),
            ("Fr. Joseph Mathew", "fr.joseph@email.com", "+91 94950 12345", "Campus Visit Request", "Greetings, I am the parish priest at St. Thomas Church, Ettumanoor. A few families in our parish are interested in Green Valley for their children. Could we arrange a group campus visit? Please suggest a convenient date."),
            ("Shalini Nair", "shalini.nair@email.com", "+91 81290 67890", "Fee Concession Query", "Respected Principal, my husband recently passed away and I am a single parent to two children studying in Grades VII and IX. I request information about any scholarship or fee-concession programmes available at the school. Kind regards, Shalini Nair."),
            ("Pradeep Menon", "pradeep.menon@email.com", "+91 70120 54321", "Coaching for Competitive Exams", "Hi, my son is in Grade X and aspires to appear for JEE Main. Does Green Valley offer integrated coaching for competitive exams alongside the CBSE curriculum? Please share the details. Thanks."),
        ]
        for name, email, phone, subject, message in submissions:
            ContactSubmission.objects.create(
                name=name, email=email, phone=phone,
                subject=subject, message=message,
                is_read=False, is_replied=False
            )
        self.stdout.write(f'  ✓ Contact Submissions ({len(submissions)})')

    # ─────────────────────────────────────────────────────────────
    #  24. PUBLIC DISCLOSURE — General Info
    # ─────────────────────────────────────────────────────────────
    def seed_general_info(self):
        GeneralInfo.objects.all().delete()
        info = [
            ("Name of the School", "Green Valley Public School", 1),
            ("Affiliation No.", "930456", 2),
            ("School Code", "42180", 3),
            ("Affiliation Valid Up To", "31 March 2030", 4),
            ("Year of Establishment", "1998", 5),
            ("Name of the Trust / Society", "Green Valley Educational Trust", 6),
            ("Trust Registration No.", "KTM/TC/1997/0453", 7),
            ("Complete Address", "Mangalam Road, Perumala Junction, Meenachil P.O., Kottayam — 686 561, Kerala, India", 8),
            ("Email", "info@greenvalleyschool.edu.in", 9),
            ("Phone", "+91 481 253 4001", 10),
            ("Fax", "+91 481 253 4099", 11),
            ("Name of the Principal", "Dr. Meera Krishnan", 12),
            ("Name of the Chairman", "Sri. K. P. Varghese", 13),
            ("Status of the School (Aided / Unaided)", "Unaided", 14),
            ("Type of School (Boys / Girls / Co-Ed)", "Co-Educational", 15),
            ("Medium of Instruction", "English", 16),
            ("Grades Having Classes", "LKG to Grade XII", 17),
        ]
        for title, value, order in info:
            GeneralInfo.objects.create(title=title, value=value, order=order, is_active=True)
        self.stdout.write(f'  ✓ General Info ({len(info)})')

    # ─────────────────────────────────────────────────────────────
    #  25. PUBLIC DISCLOSURE — Results & Academics
    # ─────────────────────────────────────────────────────────────
    def seed_results_academics(self):
        ResultsAcademics.objects.all().delete()
        results = [
            ("Grade X — CBSE Results 2025", "Pass Rate: 100% | School Average: 87.3% | Topper: Arjun S. Nair (498/500)", 1),
            ("Grade XII — CBSE Results 2025 (Science)", "Pass Rate: 99.6% | School Average: 84.8% | Topper: Ananya Thomas (496/500)", 2),
            ("Grade XII — CBSE Results 2025 (Commerce)", "Pass Rate: 100% | School Average: 86.2% | Topper: Midhun R. (489/500)", 3),
            ("Grade X — CBSE Results 2024", "Pass Rate: 100% | School Average: 85.9% | Topper: Sneha Krishnan (495/500)", 4),
            ("Grade XII — CBSE Results 2024 (Science)", "Pass Rate: 99.2% | School Average: 83.5% | Topper: Rahul Menon (492/500)", 5),
            ("Grade XII — CBSE Results 2024 (Commerce)", "Pass Rate: 100% | School Average: 85.1% | Topper: Devika S. (487/500)", 6),
            ("Staff Qualifications", "Ph.D.: 4 | M.Phil.: 8 | Post Graduate: 62 | Graduate with B.Ed.: 21 | Total Faculty: 95", 7),
            ("Student-Teacher Ratio", "20 : 1", 8),
        ]
        for title, value, order in results:
            ResultsAcademics.objects.create(
                title=title, value=value, order=order, is_active=True
            )
        self.stdout.write(f'  ✓ Results & Academics ({len(results)})')

    # ─────────────────────────────────────────────────────────────
    #  26. PUBLIC DISCLOSURE — Infrastructure
    # ─────────────────────────────────────────────────────────────
    def seed_infrastructure(self):
        Infrastructure.objects.all().delete()
        infra = [
            ("Total Campus Area", "8 Acres (32,374 sq. m)", 1),
            ("Total Built-Up Area", "45,000 sq. ft.", 2),
            ("Number of Classrooms", "65", 3),
            ("Number of Laboratories", "6 (Physics, Chemistry, Biology, Composite Science, Computer Lab ×2)", 4),
            ("STEM Innovation Centre", "1 (3,000 sq. ft.) — Robotics, AI, IoT, 3D Printing", 5),
            ("Library", "1 (5,000 sq. ft., 2 floors) — 25,000+ books, e-resources, AV room", 6),
            ("Swimming Pool", "1 (Olympic-size, 50m × 25m, 8 lanes, heated)", 7),
            ("Sports Grounds", "Cricket pitch, Football field, 400m synthetic track", 8),
            ("Indoor Sports Facility", "1 (Badminton, Table Tennis)", 9),
            ("Courts", "2 Basketball + 2 Tennis (hard court)", 10),
            ("Auditorium", "1 (600 seats, AC, Dolby Atmos sound, motorised stage)", 11),
            ("Cafeteria / Dining Hall", "1 (200 seats, FSSAI certified)", 12),
            ("Health Centre / Sick Room", "1 (Full-time nurse, visiting paediatrician, counsellor)", 13),
            ("Transport", "18 GPS-tracked, CCTV-equipped buses covering 25+ routes", 14),
            ("Solar Panels", "40% campus energy from rooftop solar installation", 15),
            ("Rainwater Harvesting Units", "6 units with total storage capacity of 1,50,000 litres", 16),
        ]
        for title, value, order in infra:
            Infrastructure.objects.create(
                title=title, value=value, order=order, is_active=True
            )
        self.stdout.write(f'  ✓ Infrastructure ({len(infra)})')

    # ─────────────────────────────────────────────────────────────
    #  27. PUBLIC DISCLOSURE — Fees
    # ─────────────────────────────────────────────────────────────
    def seed_fees(self):
        Fees.objects.all().delete()
        fees = [
            ("Pre-Primary (LKG & UKG)", "₹38,000 per annum", 1),
            ("Grades I – V", "₹48,000 per annum", 2),
            ("Grades VI – VIII", "₹55,000 per annum", 3),
            ("Grades IX – X", "₹62,000 per annum", 4),
            ("Grades XI – XII (Science)", "₹75,000 per annum", 5),
            ("Grades XI – XII (Commerce)", "₹68,000 per annum", 6),
            ("Admission Fee (One-time, Non-refundable)", "₹15,000", 7),
            ("Development Fee (Annual)", "₹5,000", 8),
            ("Transport Fee (per annum, varies by distance)", "₹18,000 – ₹30,000", 9),
            ("STEM Lab Fee (Grades V – XII, Annual)", "₹3,000", 10),
        ]
        for title, value, order in fees:
            Fees.objects.create(title=title, value=value, order=order, is_active=True)
        self.stdout.write(f'  ✓ Fees ({len(fees)})')

    # ─────────────────────────────────────────────────────────────
    #  28. SEO
    # ─────────────────────────────────────────────────────────────
    def seed_seo(self):
        PageSEO.objects.all().delete()
        seo = [
            (
                "home",
                "Green Valley Public School | Best CBSE School in Kottayam, Kerala",
                "Welcome to Green Valley Public School, a leading CBSE-affiliated institution in Kottayam, Kerala. Offering holistic education from Pre-Primary to Grade XII since 1998.",
                "green valley public school, cbse school kottayam, best school kerala, kottayam schools, cbse affiliation 930456",
            ),
            (
                "about",
                "About Us | Green Valley Public School, Kottayam",
                "Learn about the history, vision, mission, management, and campus of Green Valley Public School — nurturing young minds in Kerala since 1998.",
                "about green valley, school history, management, vision mission, kottayam",
            ),
            (
                "admissions",
                "Admissions Open 2026-27 | Green Valley Public School",
                "Apply now for admission to Green Valley Public School, Kottayam. Pre-Primary to Grade XI. Transparent, merit-based process.",
                "school admission kottayam, cbse admission kerala, green valley admissions, 2026 admissions",
            ),
            (
                "academics",
                "Academics & Curriculum | Green Valley Public School",
                "Explore our comprehensive CBSE curriculum, teaching methodology, class categories, and academic achievements at Green Valley Public School.",
                "cbse curriculum, academics, teaching methodology, stem education, green valley academics",
            ),
            (
                "facilities",
                "World-Class Facilities | Green Valley Public School",
                "State-of-the-art facilities including smart classrooms, science labs, STEM centre, Olympic swimming pool, auditorium, and more at Green Valley.",
                "school facilities, smart classrooms, swimming pool, stem lab, sports complex, kottayam",
            ),
            (
                "gallery",
                "Photo Gallery | Green Valley Public School",
                "Browse photos of campus life, events, sports, cultural celebrations, and facilities at Green Valley Public School, Kottayam.",
                "school gallery, photos, campus, events, cultural, sports, green valley",
            ),
            (
                "contact",
                "Contact Us | Green Valley Public School, Kottayam",
                "Get in touch with Green Valley Public School. Address, phone, email, and location map for our Kottayam campus.",
                "contact green valley, school address, phone number, kottayam, directions",
            ),
            (
                "notices",
                "Notices & Circulars | Green Valley Public School",
                "Stay updated with the latest notices, circulars, and announcements from Green Valley Public School, Kottayam.",
                "school notices, circulars, announcements, green valley, cbse notices",
            ),
            (
                "events",
                "Events & News | Green Valley Public School",
                "Discover upcoming events, cultural programmes, sports meets, and news at Green Valley Public School.",
                "school events, annual day, sports meet, cultural programme, green valley news",
            ),
            (
                "achievements",
                "Achievements | Green Valley Public School",
                "Celebrating academic, sports, and cultural achievements of students and faculty at Green Valley Public School, Kottayam.",
                "school achievements, board results, science olympiad, sports awards, green valley",
            ),
            (
                "public-disclosure",
                "CBSE Public Disclosure | Green Valley Public School",
                "Mandatory public disclosure information as per CBSE requirements — affiliation, fees, infrastructure, and results.",
                "cbse mandatory disclosure, affiliation, fees structure, school information, green valley",
            ),
        ]
        for slug, title, desc, keywords in seo:
            PageSEO.objects.create(
                page_slug=slug, title=title,
                meta_description=desc, meta_keywords=keywords,
            )
        self.stdout.write(f'  ✓ Page SEO ({len(seo)})')
