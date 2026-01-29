"""
Management command to seed the database with dummy data.
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
        self.seed_contact_page()
        self.seed_contact_submissions()
        self.seed_public_disclosure()
        self.seed_seo()

        self.stdout.write(self.style.SUCCESS('\n✅ Database seeded successfully!'))

    def seed_site_settings(self):
        settings, created = SiteSettings.objects.get_or_create(pk=1)
        settings.school_name = "Dummy School"
        settings.school_motto = "Excellence in Education"
        settings.school_address = "123 Education Lane, Knowledge City, State 12345"
        settings.school_phone = "+91 98765 43210, +91 98765 43219"
        settings.school_email = "info@sunrisepublicschool.edu"
        settings.school_logo = 'placeholder.png'
        settings.favicon = 'placeholder.png'
        settings.school_hours = "Monday - Friday: 8:00 AM - 2:00 PM, Saturday: 8:00 AM - 12:00 PM"
        settings.office_hours = "Monday - Friday: 9:00 AM - 4:00 PM, Saturday: 9:00 AM - 1:00 PM"
        settings.facebook_url = "https://facebook.com/sunriseschool"
        settings.twitter_url = "https://twitter.com/sunriseschool"
        settings.instagram_url = "https://instagram.com/sunriseschool"
        settings.youtube_url = "https://youtube.com/sunriseschool"
        settings.footer_text = "© 2024 Dummy School. All rights reserved."
        settings.save()
        self.stdout.write('  ✓ Site settings')

    def seed_hero_section(self):
        hero, created = HeroSection.objects.get_or_create(pk=1)
        hero.title = "Welcome to Dummy School"
        hero.subtitle = "Nurturing minds, building futures. Join us in our journey of excellence in education where every student is empowered to reach their full potential."
        hero.cta_text = "Explore More"
        hero.cta_link = "/about"
        hero.image = 'placeholder.png'
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
        about.title = "About Dummy School"
        about.content = "Established in 2010, Dummy School has been at the forefront of quality education. With state-of-the-art facilities and a dedicated faculty, we provide an environment that encourages academic excellence and holistic development."
        about.established_year = 2010
        about.students_count = "1500+"
        about.teachers_count = "75+"
        about.save()
        self.stdout.write('  ✓ About section')

    def seed_principal_message(self):
        pm, created = PrincipalMessage.objects.get_or_create(pk=1)
        pm.name = "Dr. Rajesh Kumar"
        pm.title = "Principal"
        pm.message = "Dear Parents and Students,\n\nWelcome to Dummy School! Education is not just about academics; it's about nurturing well-rounded individuals who can contribute to society. At our school, we believe in fostering creativity, critical thinking, and character development.\n\nOur dedicated faculty works tirelessly to provide the best learning environment for your children. We look forward to partnering with you in this educational journey.\n\nWarm regards,\nDr. Rajesh Kumar"
        pm.qualification = "Ph.D. in Education, M.Ed., B.Ed."
        pm.photo = 'placeholder.png'
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
                publish_date=timezone.now().date() - timedelta(days=random.randint(0, 30)),
                attachment='placeholder.png'
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
                status='published',
                image='placeholder.png'
            )
        self.stdout.write('  ✓ Events')

    def seed_gallery(self):
        categories = ["Annual Day", "Sports", "Science Fair", "Cultural Events", "Campus Life"]
        GalleryImage.objects.all().delete()
        GalleryCategory.objects.all().delete()
        for i, name in enumerate(categories):
            cat = GalleryCategory.objects.create(name=name, order=i)
            # Add dummy images for each category
            for j in range(3):
                GalleryImage.objects.create(
                    category=cat,
                    title=f"{name} Image {j+1}",
                    caption=f"{name} Description {j+1}",
                    image='placeholder.png',
                    order=j
                )
        self.stdout.write('  ✓ Gallery categories & images')

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
            fac = Facility.objects.create(
                name=name,
                short_description=desc,
                icon=icon,
                order=i,
                is_active=True,
                cover_image='placeholder.png'
            )
            # Add dummy images for facility
            for j in range(2):
                FacilityImage.objects.create(
                    facility=fac,
                    caption=f"{name} View {j+1}",
                    image='placeholder.png',
                    order=j
                )
        self.stdout.write('  ✓ Facilities & images')

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
                is_active=True,
                image='placeholder.png'
            )
        self.stdout.write('  ✓ Achievements')

    def seed_testimonials(self):
        testimonials_data = [
            ("Priya Sharma", "Parent", "The school has provided an excellent learning environment for my child. The teachers are dedicated and the overall development approach is commendable."),
            ("Rahul Verma", "Alumni - Batch 2020", "My years at Dummy School were transformative. The values and education I received here shaped my future success."),
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
        Documentation.objects.all().delete()
        for i, (title, desc, category) in enumerate(downloads_data):
            Documentation.objects.create(
                title=title,
                description=desc,
                # category=category, # Removed as Documentation model doesn't have category
                order=i,
                is_active=True
            )
        self.stdout.write('  ✓ Downloads (Documentation)')

    def seed_academics(self):
        page, _ = AcademicsPage.objects.get_or_create(pk=1)
        page.hero_title = "Academics"
        page.hero_subtitle = "Our comprehensive curriculum is designed to nurture intellectual curiosity and prepare students for the challenges of tomorrow."
        page.overview_content = "We offer a balanced education that combines academic rigor with creative exploration. Our students are encouraged to ask questions, think critically, and apply their knowledge to real-world problems."
        page.curriculum_content = "The school follows the CBSE curriculum, enriched with additional resources and activities to provide a holistic learning experience. We offer a wide range of subjects to cater to the diverse interests of our students."
        page.methodology_content = "Our teaching methodology is student-centered, focusing on experiential learning and active participation. We use a variety of teaching aids and technology to make learning engaging and effective."
        page.hero_image = 'placeholder.png'
        page.save()

        # Categories
        ClassCategory.objects.all().delete()
        categories = [
            ("Primary (I-V)", "Foundation years focusing on basic literacy, numeracy, and creativity.", 1, ["English", "Mathematics", "EVS", "Arts", "Music"]),
            ("Middle (VI-VIII)", "Building critical thinking and subject expertise.", 2, ["English", "Mathematics", "Science", "Social Science", "Hindi", "Computer Science"]),
            ("Secondary (IX-X)", "Board exam preparation with comprehensive coverage.", 3, ["English", "Mathematics", "Science", "Social Science", "Hindi/Sanskrit"]),
            ("Senior Secondary (XI-XII)", "Specialized streams - Science, Commerce, and Humanities.", 4, ["Physics", "Chemistry", "Mathematics", "Biology", "Accountancy", "Business Studies", "Economics"]),
        ]
        
        # Clear Subjects first
        Subject.objects.all().delete()
        
        for name, desc, order, subjects_list in categories:
            cat = ClassCategory.objects.create(name=name, description=desc, order=order, image='placeholder.png')
            for i, sub_name in enumerate(subjects_list):
                 sub, _ = Subject.objects.get_or_create(name=sub_name, defaults={'icon': '📚'})
                 sub.categories.add(cat)

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

        self.stdout.write('  ✓ Academics (Categories & Subjects)')

    def seed_admissions(self):
        settings, _ = AdmissionSettings.objects.get_or_create(pk=1)
        settings.is_open = True
        settings.hero_title = "Admissions Open 2025-26"
        settings.hero_subtitle = "Nurturing minds, building futures. Join our community of learners!"
        settings.overview_title = "Admission Process Overview"
        settings.overview_content = "We are now accepting applications for the academic year 2025-26. Our admission process is designed to be transparent and straightforward."
        settings.eligibility_title = "Eligibility & Documents"
        settings.eligibility_content = "Students must be of appropriate age for the class applied. Please ensure all required documents are ready for submission."
        settings.documents_required = "Birth Certificate\nPrevious School TC\nAddress Proof\nPassport Photos\nAadhar Card"
        settings.contact_info = "Email: admissions@sunrisepublicschool.edu\nPhone: +91 98765 43211\nOffice Hours: 9:00 AM - 3:00 PM"
        settings.application_form_link = "https://forms.gle/dummy-admission-form"
        settings.hero_image = 'placeholder.png'
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
        page.history_content = "Dummy School was established in 2010 with a vision to provide quality education. Over the years, we have grown to become one of the leading schools in the region."
        page.history_image = 'placeholder.png'
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
            ManagementMember.objects.create(
                name=name, position=role, bio=bio, order=order,
                photo='placeholder.png'
            )

        self.stdout.write('  ✓ About page')

    def seed_public_disclosure(self):
        # General Info
        GeneralInfo.objects.all().delete()
        general = [
            ("School Name", "Dummy School"),
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

    def seed_contact_page(self):
        page, _ = ContactPage.objects.get_or_create(pk=1)
        page.hero_title = "Get In Touch"
        page.hero_subtitle = "We'd love to hear from you. Reach out to us for any inquiries or to visit our campus."
        page.map_embed_code = '<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3502.1!2d77.2!3d28.6!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMjjCsDM2JzAwLjAiTiA3N8KwMTInMDAuMCJF!5e0!3m2!1sen!2sin!4v1!5m2!1sen!2sin" width="100%" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>'
        page.save()
        self.stdout.write('  ✓ Contact page')

    def seed_contact_submissions(self):
        ContactSubmission.objects.all().delete()
        submissions = [
            ("John Doe", "john@example.com", "9876543210", "Admission Inquiry", "I want to know about the admission process for Grade 5."),
            ("Jane Smith", "jane@example.com", "9876543211", "Fee Structure", "Could you please provide the detailed fee structure for Grade 11?"),
            ("Alice Brown", "alice@example.com", "9876543212", "Campus Visit", "I would like to schedule a visit to the school campus next Monday."),
        ]
        for name, email, phone, subject, message in submissions:
            ContactSubmission.objects.create(
                name=name, email=email, phone=phone,
                subject=subject, message=message
            )
        self.stdout.write('  ✓ Contact submissions')

    def seed_seo(self):
        seo_data = [
            ("home", "Best CBSE School | Dummy School", "Welcome to Dummy School, a center of excellence in education. Nurturing young minds for a brighter future.", "school, education, cbse, best school"),
            ("about", "About Us | Dummy School", "Learn about our history, vision, mission, and the dedicated team behind Dummy School.", "about us, history, vision, mission"),
            ("admissions", "Admissions Open | Dummy School", "Join the Sunrise family. Admissions open for the academic year 2025-26. Apply now!", "admissions, apply now, school admission"),
            ("academics", "Academics & Curriculum | Dummy School", "Explore our comprehensive curriculum designed to foster critical thinking and holistic development.", "academics, curriculum, syllabus, education"),
            ("contact", "Contact Us | Dummy School", "Get in touch with us. We are happy to answer your queries and welcome you to our campus.", "contact, address, phone, email"),
            ("gallery", "Photo Gallery | Dummy School", "Glimpses of life at Dummy School. Events, celebrations, infrastructure, and more.", "gallery, photos, events, school life"),
            ("notices", "Notices & Announcements | Dummy School", "Stay updated with the latest news, circulars, and announcements from the school.", "notices, announcements, news, circulars"),
            ("events", "Upcoming Events | Dummy School", "Check out our upcoming events and participate in the vibrant school community activities.", "events, calendar, school activities"),
            ("facilities", "World-Class Facilities | Dummy School", "State-of-the-art infrastructure including smart classrooms, labs, libraries, and sports complex.", "facilities, infrastructure, labs, library"),
        ]
        PageSEO.objects.all().delete()
        for slug, title, desc, keywords in seo_data:
            PageSEO.objects.create(
                page_slug=slug,
                title=title,
                meta_description=desc,
                meta_keywords=keywords
            )
        self.stdout.write('  ✓ SEO Data')
