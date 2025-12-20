"""
Management command to seed the database with dummy data.
"""
import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone

from content.models import (
    SiteSettings, HeroSection, VisionMission, HomeAboutSection,
    PrincipalMessage, QuickLink,
    Notice, Event, GalleryCategory, GalleryImage,
    Facility, Achievement, Testimonial, Download,
    AcademicsPage, ClassCategory, Subject, AcademicHighlight,
    AdmissionSettings, AdmissionStep,
    AboutPage, TimelineEvent, ManagementMember,
    GeneralInfo, ResultsAcademics, Infrastructure, Fees
)


class Command(BaseCommand):
    help = 'Populate database with dummy data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database with dummy data...\n')

        # Site Settings
        self.seed_site_settings()
        self.seed_hero_section()
        self.seed_vision_mission()
        self.seed_about_section()
        self.seed_principal_message()
        self.seed_quick_links()

        # Content
        self.seed_notices()
        self.seed_events()
        self.seed_gallery()
        self.seed_facilities()
        self.seed_achievements()
        self.seed_testimonials()
        self.seed_downloads()
        self.seed_academics()
        self.seed_admissions()
        self.seed_about_page()
        self.seed_public_disclosure()

        self.stdout.write(self.style.SUCCESS('\n✅ Database seeded successfully!'))

    def seed_site_settings(self):
        settings, created = SiteSettings.objects.get_or_create(pk=1)
        settings.school_name = "Sunrise Public School"
        settings.school_motto = "Excellence in Education"
        settings.address = "123 Education Lane, Knowledge City, State 12345"
        settings.phone = "+91 98765 43210"
        settings.email = "info@sunrisepublicschool.edu"
        settings.facebook_url = "https://facebook.com/sunriseschool"
        settings.twitter_url = "https://twitter.com/sunriseschool"
        settings.instagram_url = "https://instagram.com/sunriseschool"
        settings.youtube_url = "https://youtube.com/sunriseschool"
        settings.footer_text = "© 2024 Sunrise Public School. All rights reserved."
        settings.save()
        self.stdout.write('  ✓ Site settings')

    def seed_hero_section(self):
        hero, created = HeroSection.objects.get_or_create(pk=1)
        hero.title = "Welcome to Sunrise Public School"
        hero.subtitle = "Nurturing minds, building futures. Join us in our journey of excellence in education where every student is empowered to reach their full potential."
        hero.cta_text = "Explore More"
        hero.cta_link = "/about"
        hero.save()
        self.stdout.write('  ✓ Hero section')

    def seed_vision_mission(self):
        vm, created = VisionMission.objects.get_or_create(pk=1)
        vm.vision_title = "Our Vision"
        vm.vision_content = "To be a leading institution of academic excellence, nurturing global citizens who contribute positively to society through innovation, creativity, and ethical leadership."
        vm.mission_title = "Our Mission"
        vm.mission_content = "To provide a holistic education that develops intellectual curiosity, critical thinking, and a passion for lifelong learning in a nurturing and inclusive environment."
        vm.values_title = "Our Values"
        vm.values_content = "Integrity\nExcellence\nRespect\nInnovation\nCollaboration\nCompassion"
        vm.save()
        self.stdout.write('  ✓ Vision & Mission')

    def seed_about_section(self):
        # NOTE: Renamed model AboutSection -> HomeAboutSection
        about, created = HomeAboutSection.objects.get_or_create(pk=1)
        about.title = "About Sunrise Public School"
        about.content = "Established in 2010, Sunrise Public School has been at the forefront of quality education. With state-of-the-art facilities and a dedicated faculty, we provide an environment that encourages academic excellence and holistic development."
        about.established_year = 2010
        about.students_count = "1500+"
        about.teachers_count = "75+"
        about.save()
        self.stdout.write('  ✓ About section')

    def seed_principal_message(self):
        pm, created = PrincipalMessage.objects.get_or_create(pk=1)
        pm.name = "Dr. Rajesh Kumar"
        pm.title = "Principal"
        pm.message = "Dear Parents and Students,\n\nWelcome to Sunrise Public School! Education is not just about academics; it's about nurturing well-rounded individuals who can contribute to society. At our school, we believe in fostering creativity, critical thinking, and character development.\n\nOur dedicated faculty works tirelessly to provide the best learning environment for your children. We look forward to partnering with you in this educational journey.\n\nWarm regards,\nDr. Rajesh Kumar"
        pm.qualification = "Ph.D. in Education, M.Ed., B.Ed."
        pm.save()
        self.stdout.write('  ✓ Principal message')

    def seed_quick_links(self):
        links = [
            ("About Us", "/about", 1),
            ("Admissions", "/admissions", 2),
            ("Academics", "/academics", 3),
            ("Gallery", "/gallery", 4),
            ("Contact", "/contact", 5),
            ("Downloads", "/downloads", 6),
        ]
        QuickLink.objects.all().delete()
        for title, url, order in links:
            QuickLink.objects.create(title=title, url=url, order=order, is_active=True)
        self.stdout.write('  ✓ Quick links')

    def seed_notices(self):
        notices_data = [
            ("Annual Day Celebration", "We are delighted to announce our Annual Day celebration on January 15th, 2025. All parents are cordially invited to join us for an evening of cultural performances and prize distribution.", True),
            ("Winter Vacation Notice", "The school will remain closed for winter vacation from December 25th to January 1st. Classes will resume on January 2nd, 2025.", True),
            ("Parent-Teacher Meeting", "A PTM is scheduled for January 10th, 2025. Parents are requested to attend and discuss their ward's progress with the respective class teachers.", False),
            ("Sports Day Registration", "Registration for the Annual Sports Day is now open. Students interested in participating should register with their Physical Education teacher.", False),
            ("Science Exhibition", "The inter-class Science Exhibition will be held on February 5th. Students are encouraged to start preparing their projects.", False),
        ]
        Notice.objects.all().delete()
        for title, content, is_important in notices_data:
            Notice.objects.create(
                title=title,
                content=content,
                is_important=is_important,
                status='published',
                publish_date=timezone.now().date() - timedelta(days=random.randint(0, 30))
            )
        self.stdout.write('  ✓ Notices')

    def seed_events(self):
        events_data = [
            ("Annual Sports Day 2025", "Our annual sports day featuring track and field events, team sports, and fun activities for all age groups.", "Join us for an exciting day of sportsmanship and healthy competition."),
            ("Science Fair", "Students showcase their innovative science projects and experiments. Open for all parents and visitors.", "Witness the creativity of young minds at our annual science fair."),
            ("Republic Day Celebration", "Special assembly and cultural program to celebrate Republic Day with patriotic performances.", "Celebrating the spirit of our nation."),
            ("Inter-School Debate Competition", "Students from various schools compete in debates on contemporary topics.", "Watch our students showcase their oratory skills."),
            ("Art Exhibition", "A display of artwork created by students across all grades throughout the year.", "Experience the artistic talents of our students."),
        ]
        Event.objects.all().delete()
        for i, (title, content, excerpt) in enumerate(events_data):
            # Create a slug manually or let save() handle it if handled
            # Assuming save() handles it or it's not strictly required by model if blank=True
            Event.objects.create(
                title=title,
                content=content,
                excerpt=excerpt,
                event_date=timezone.now().date() + timedelta(days=random.randint(1, 90)),
                is_featured=(i < 2),
                status='published'
            )
        self.stdout.write('  ✓ Events')

    def seed_gallery(self):
        categories = ["Annual Day", "Sports", "Science Fair", "Cultural Events", "Campus Life"]
        GalleryImage.objects.all().delete()
        GalleryCategory.objects.all().delete()
        for i, name in enumerate(categories):
            GalleryCategory.objects.create(name=name, order=i)
        self.stdout.write('  ✓ Gallery categories')

    def seed_facilities(self):
        facilities_data = [
            ("Smart Classrooms", "Air-conditioned classrooms equipped with interactive whiteboards and projectors for enhanced learning.", "💻"),
            ("Science Laboratories", "Well-equipped Physics, Chemistry, and Biology labs for hands-on practical learning.", "🔬"),
            ("Computer Lab", "Modern computer lab with high-speed internet and latest software for digital literacy.", "🖥️"),
            ("Library", "Extensive collection of books, journals, and digital resources for research and reading.", "📚"),
            ("Sports Complex", "Multi-purpose sports ground with facilities for cricket, football, basketball, and athletics.", "⚽"),
            ("Auditorium", "500-seater air-conditioned auditorium for cultural events and assemblies.", "🎭"),
            ("Cafeteria", "Hygienic cafeteria serving nutritious meals and snacks.", "🍽️"),
            ("Transportation", "Safe and reliable bus service covering all major routes in the city.", "🚌"),
        ]
        Facility.objects.all().delete()
        for i, (name, desc, icon) in enumerate(facilities_data):
            Facility.objects.create(
                name=name,
                short_description=desc,
                icon=icon,
                order=i,
                is_active=True
            )
        self.stdout.write('  ✓ Facilities')

    def seed_achievements(self):
        achievements_data = [
            ("Best School Award", "Awarded Best School in the district by the State Education Board.", "2024"),
            ("100% Board Results", "All students passed the Class 10 and 12 board exams with flying colors.", "2024"),
            ("National Science Olympiad", "5 students qualified for the national round of Science Olympiad.", "2023"),
            ("Inter-School Sports Champion", "Won the overall championship in district-level inter-school sports meet.", "2023"),
            ("Green School Certification", "Received Green School certification for environmental initiatives.", "2022"),
        ]
        Achievement.objects.all().delete()
        for i, (title, desc, year) in enumerate(achievements_data):
            Achievement.objects.create(
                title=title,
                description=desc,
                year=year,
                order=i,
                is_active=True
            )
        self.stdout.write('  ✓ Achievements')

    def seed_testimonials(self):
        testimonials_data = [
            ("Priya Sharma", "Parent", "The school has provided an excellent learning environment for my child. The teachers are dedicated and the overall development approach is commendable."),
            ("Rahul Verma", "Alumni - Batch 2020", "My years at Sunrise Public School were transformative. The values and education I received here shaped my future success."),
            ("Mrs. Sunita Patel", "Parent", "Outstanding faculty and wonderful facilities. My children love going to school every day!"),
            ("Amit Kumar", "Alumni - Batch 2018", "The school not only focused on academics but also nurtured my talents in sports and arts."),
        ]
        Testimonial.objects.all().delete()
        for name, role, content in testimonials_data:
            Testimonial.objects.create(
                name=name,
                role=role,
                content=content,
                is_active=True
            )
        self.stdout.write('  ✓ Testimonials')

    def seed_downloads(self):
        downloads_data = [
            ("Admission Form 2025-26", "Download the admission form for the upcoming academic year.", "admission"),
            ("Fee Structure 2024-25", "Detailed fee structure for all classes.", "fee"),
            ("School Calendar 2024-25", "Academic calendar with important dates and holidays.", "calendar"),
            ("Holiday List 2024-25", "List of holidays for the current academic year.", "holiday"),
            ("School Prospectus", "Complete information about our school, programs, and facilities.", "prospectus"),
        ]
        Download.objects.all().delete()
        for title, desc, category in downloads_data:
            Download.objects.create(
                title=title,
                description=desc,
                category=category,
                is_active=True
            )
        self.stdout.write('  ✓ Downloads')

    def seed_academics(self):
        # Page
        page, _ = AcademicsPage.objects.get_or_create(pk=1)
        page.page_title = "Academics"
        page.page_description = "Our comprehensive curriculum is designed to nurture intellectual curiosity and prepare students for the challenges of tomorrow."
        page.save()

        # Categories
        ClassCategory.objects.all().delete()
        categories = [
            ("Primary (I-V)", "Foundation years focusing on basic literacy, numeracy, and creativity.", 1),
            ("Middle (VI-VIII)", "Building critical thinking and subject expertise.", 2),
            ("Secondary (IX-X)", "Board exam preparation with comprehensive coverage.", 3),
            ("Senior Secondary (XI-XII)", "Specialized streams - Science, Commerce, and Humanities.", 4),
        ]
        for name, desc, order in categories:
            ClassCategory.objects.create(name=name, description=desc, order=order)

        # Academic Highlights
        AcademicHighlight.objects.all().delete()
        highlights = [
            ("Pass Rate", "99%", "🎓"),
            ("Distinction Rate", "75%", "⭐"),
            ("Board Toppers", "25+", "🏆"),
            ("Faculty Members", "75+", "👨‍🏫"),
        ]
        for i, (title, value, icon) in enumerate(highlights):
            AcademicHighlight.objects.create(title=title, value=value, icon=icon, order=i)

        self.stdout.write('  ✓ Academics')

    def seed_admissions(self):
        settings, _ = AdmissionSettings.objects.get_or_create(pk=1)
        settings.is_open = True
        settings.title = "Admissions Open 2025-26"
        settings.description = "We are now accepting applications for the academic year 2025-26. Join our community of learners!"
        settings.eligibility_info = "Students must be of appropriate age for the class applied."
        settings.required_documents = "Birth Certificate\nPrevious School TC\nAddress Proof\nPassport Photos\nAadhar Card"
        settings.contact_email = "admissions@sunrisepublicschool.edu"
        settings.contact_phone = "+91 98765 43211"
        settings.save()

        AdmissionStep.objects.all().delete()
        steps = [
            ("Submit Application", "Fill out the online application form with required details.", 1),
            ("Document Verification", "Submit required documents for verification.", 2),
            ("Entrance Test", "Appear for the entrance assessment (for classes III onwards).", 3),
            ("Interview", "Attend the personal interview with parents.", 4),
            ("Fee Payment", "Complete the admission by paying the required fees.", 5),
        ]
        for title, desc, order in steps:
            AdmissionStep.objects.create(title=title, description=desc, order=order)

        self.stdout.write('  ✓ Admissions')

    def seed_about_page(self):
        page, _ = AboutPage.objects.get_or_create(pk=1)
        page.page_title = "About Us"
        page.page_description = "Learn about our rich history, values, and commitment to excellence in education."
        page.history_content = "Sunrise Public School was established in 2010 with a vision to provide quality education. Over the years, we have grown to become one of the leading schools in the region."
        page.save()

        TimelineEvent.objects.all().delete()
        timeline = [
            (2010, "Foundation", "School established with 100 students and 10 teachers."),
            (2013, "Expansion", "New building inaugurated with additional facilities."),
            (2015, "Excellence", "Received Best School Award from State Government."),
            (2018, "Digital Transformation", "All classrooms converted to smart classrooms."),
            (2020, "Milestone", "Crossed 1000+ student strength with 100% board results."),
            (2023, "Recognition", "Awarded Green School certification."),
        ]
        for year, title, desc in timeline:
            TimelineEvent.objects.create(year=str(year), title=title, description=desc)

        ManagementMember.objects.all().delete()
        members = [
            ("Dr. Suresh Sharma", "Chairman", "Founder and visionary leader of the institution.", 1),
            ("Mrs. Kavita Sharma", "Vice Chairperson", "Oversees academic excellence and student welfare.", 2),
            ("Dr. Rajesh Kumar", "Principal", "Leads the academic and administrative functions.", 3),
            ("Mr. Anand Singh", "Administrator", "Manages day-to-day operations.", 4),
        ]
        for name, role, bio, order in members:
            ManagementMember.objects.create(name=name, position=role, bio=bio, order=order)

        self.stdout.write('  ✓ About page')

    def seed_public_disclosure(self):
        # General Info
        GeneralInfo.objects.all().delete()
        general = [
            ("School Name", "Sunrise Public School"),
            ("Affiliation No.", "CBSE/123456/2010"),
            ("School Code", "12345"),
            ("Year of Establishment", "2010"),
            ("Address", "123 Education Lane, Knowledge City, State 12345"),
            ("Email", "info@sunrisepublicschool.edu"),
            ("Phone", "+91 98765 43210"),
        ]
        for title, value in general:
            GeneralInfo.objects.create(title=title, value=value)

        # Infrastructure
        Infrastructure.objects.all().delete()
        infra = [
            ("Total Campus Area", "5 Acres"),
            ("Built Up Area", "25,000 Sq. Ft."),
            ("No. of Classrooms", "60"),
            ("No. of Laboratories", "8"),
            ("Library Capacity", "10,000 Books"),
            ("Computer Systems", "150"),
        ]
        for title, value in infra:
            Infrastructure.objects.create(title=title, value=value)

        # Fees
        Fees.objects.all().delete()
        fees = [
            ("Classes I-V", "₹45,000 per annum"),
            ("Classes VI-VIII", "₹52,000 per annum"),
            ("Classes IX-X", "₹60,000 per annum"),
            ("Classes XI-XII (Science)", "₹72,000 per annum"),
            ("Classes XI-XII (Commerce)", "₹65,000 per annum"),
        ]
        for title, value in fees:
            Fees.objects.create(title=title, value=value)

        self.stdout.write('  ✓ Public disclosure')
