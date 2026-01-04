from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from content.models import (
    SiteSettings, HeroSection, PrincipalMessage, HomeAboutSection,
    VisionMission, AboutPage, AcademicsPage, Notice, Event,
    GalleryCategory, GalleryImage, Facility, Testimonial, Achievement,
    GeneralInfo, Infrastructure, Fees, ResultsAcademics,
    AdmissionSettings, AdmissionStep, ManagementMember, TimelineEvent, QuickLink
)
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = 'Fills all content manager fields with dummy data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Filling content with dummy data...')

        # 1. Site Settings
        settings, _ = SiteSettings.objects.get_or_create()
        settings.school_name = "Sunrise Public School"
        settings.school_motto = "Excellence through Education"
        settings.school_address = "123 Education Lane, Knowledge City, State - 400001"
        settings.school_phone = "+91 98765 43210"
        settings.school_email = "admin@sunrisepublic.edu"
        settings.footer_text = "© 2025 Sunrise Public School. All rights reserved. Shaping minds for a better tomorrow."
        settings.facebook_url = "https://facebook.com/sunrisepublic"
        settings.twitter_url = "https://twitter.com/sunrisepublic"
        settings.instagram_url = "https://instagram.com/sunrisepublic"
        settings.youtube_url = "https://youtube.com/sunrisepublic"
        settings.save()
        self.stdout.write(self.style.SUCCESS('Site Settings filled.'))

        # 2. Hero Section
        hero, _ = HeroSection.objects.get_or_create()
        hero.title = "Welcome to Sunrise Public School"
        hero.subtitle = "Where we nurture curiosity and build character. Join us in our journey of excellence."
        hero.cta_text = "Admissions Open"
        hero.cta_link = "/admissions"
        # Dummy image handling
        if not hero.image:
             hero.image.save('hero_dummy.jpg', ContentFile(b'dummy_image_data'), save=False)
        hero.save()
        self.stdout.write(self.style.SUCCESS('Hero Section filled.'))

        # 3. Principal Message
        principal, _ = PrincipalMessage.objects.get_or_create()
        principal.name = "Dr. Rajesh Sharma"
        principal.title = "Principal"
        principal.qualification = "M.Sc., B.Ed., Ph.D. in Education"
        principal.message = (
            "Welcome to our school. We believe in holistic development of every child. "
            "Our focus is not just on academics but on character building, sports, and arts. "
            "We strive to create global citizens who are rooted in their values."
        )
        if not principal.photo:
            principal.photo.save('principal_dummy.jpg', ContentFile(b'dummy_image_data'), save=False)
        principal.save()
        self.stdout.write(self.style.SUCCESS('Principal Message filled.'))

        # 4. Home About Section (Stats)
        home_about, _ = HomeAboutSection.objects.get_or_create()
        home_about.title = "About Our School"
        home_about.content = (
            "Founded in 1995, Sunrise Public School has been a beacon of knowledge. "
            "We provide a nurturing environment where students can thrive academically and socially."
        )
        home_about.established_year = 1995
        home_about.students_count = "2500+"
        home_about.teachers_count = "150+"
        if not home_about.image:
             home_about.image.save('about_dummy.jpg', ContentFile(b'dummy_image_data'), save=False)
        home_about.save()
        self.stdout.write(self.style.SUCCESS('Home About Section filled.'))

        # 5. Vision & Mission
        vm, _ = VisionMission.objects.get_or_create()
        vm.vision_title = "Our Vision"
        vm.vision_content = "To be a leading institution that fosters innovation and ethical leadership."
        vm.mission_title = "Our Mission"
        vm.mission_content = "To provide quality education that empowers students to reach their full potential."
        vm.values_title = "Core Values"
        vm.values_content = "Integrity, Excellence, Respect, and Collaboration."
        vm.save()
        self.stdout.write(self.style.SUCCESS('Vision & Mission filled.'))

        # 6. About Page (Detail)
        about_page, _ = AboutPage.objects.get_or_create()
        about_page.hero_title = "About Us"
        about_page.hero_subtitle = "Learn about our rich history and state-of-the-art facilities."
        about_page.history_title = "Our History"
        about_page.history_content = (
            "Sunrise Public School started as a small initiative with just 50 students. "
            "Over the decades, we have grown into a premier institution. "
            "Our journey has been marked by continuous improvement and dedication to student success."
        )
        about_page.infrastructure_title = "World-Class Infrastructure"
        about_page.infrastructure_content = (
            "Our campus spans 10 acres with smart classrooms, advanced labs for Physics, Chemistry, and Biology. "
            "We have a vast library, a sports complex with swimming pool, and an auditorium."
        )

        about_page.save()
        self.stdout.write(self.style.SUCCESS('About Page filled.'))

        # 7. Academics Page
        academics, _ = AcademicsPage.objects.get_or_create()
        academics.hero_title = "Academics"
        academics.hero_subtitle = "Pursuing Academic Excellence"
        
        academics.curriculum_title = "Our Curriculum"
        academics.curriculum_content = (
            "We follow the CBSE curriculum, enriched with project-based learning. "
            "Our curriculum is designed to challenge students and foster critical thinking."
        )
        
        academics.methodology_title = "Teaching Methodology"
        academics.methodology_content = (
            "We use a blend of traditional and modern teaching methods. "
            "Interactive sessions, digital learning tools, and experiential learning are key components."
        )
        
        academics.calendar_title = "Academic Calendar 2025-26"
        
        if not academics.curriculum_image:
             academics.curriculum_image.save('curriculum_dummy.jpg', ContentFile(b'dummy_image_data'), save=False)
        
        if not academics.calendar_file:
             academics.calendar_file.save('calendar_dummy.pdf', ContentFile(b'dummy_pdf_data'), save=False)

        academics.save()
        self.stdout.write(self.style.SUCCESS('Academics Page filled.'))



        # 9. Notices
        if not Notice.objects.exists():
            Notice.objects.create(
                title="Winter Break Announcement",
                content="The school will remain closed for winter break from Dec 25th to Jan 5th.",
                is_important=True,
                publish_date=date.today()
            )
            Notice.objects.create(
                title="Parent-Teacher Meeting",
                content="PTM for Classes I-V will be held on Saturday, Jan 10th.",
                publish_date=date.today()
            )
        self.stdout.write(self.style.SUCCESS('Notices filled.'))

        # 10. Events
        if not Event.objects.exists():
            Event.objects.create(
                title="Annual Sports Day 2025",
                content="Join us for a day of athleticism and team spirit.",
                event_date=date.today() + timedelta(days=30),
                is_featured=True
            )
            Event.objects.create(
                title="Science Exhibition",
                content="Students showcasing their innovative science projects.",
                event_date=date.today() + timedelta(days=15)
            )
        self.stdout.write(self.style.SUCCESS('Events filled.'))

        # 11. General Info
        if not GeneralInfo.objects.exists():
            GeneralInfo.objects.create(title="School Name", value="Sunrise Public School", order=1)
            GeneralInfo.objects.create(title="Affiliation Number", value="CBSE/AFF/123456", order=2)
            GeneralInfo.objects.create(title="School Code", value="54321", order=3)
            GeneralInfo.objects.create(title="Address", value="123 Education Lane, Knowledge City", order=4)
            GeneralInfo.objects.create(title="Principal", value="Dr. Rajesh Sharma", order=5)
            GeneralInfo.objects.create(title="School Email", value="admin@sunrisepublic.edu", order=6)
            GeneralInfo.objects.create(title="School Phone", value="+91 98765 43210", order=7)
        self.stdout.write(self.style.SUCCESS('General Info filled.'))

        # 12. Infrastructure
        if not Infrastructure.objects.exists():
            Infrastructure.objects.create(title="Total Campus Area", value="10 Acres", order=1)
            Infrastructure.objects.create(title="Built-up Area", value="5000 Sq. Meters", order=2)
            Infrastructure.objects.create(title="Playground Area", value="3000 Sq. Meters", order=3)
            Infrastructure.objects.create(title="Number of Classrooms", value="50", order=4)
            Infrastructure.objects.create(title="Labs", value="Physics, Chemistry, Biology, Computer, Math", order=5)
            Infrastructure.objects.create(title="Library", value="1500 Sq. Ft with 5000+ Books", order=6)
        self.stdout.write(self.style.SUCCESS('Infrastructure filled.'))

        # 13. Fees
        if not Fees.objects.exists():
            Fees.objects.create(title="Admission Fee", value="Rs. 10,000 (One time)", order=1)
            Fees.objects.create(title="Tuition Fee (Primary)", value="Rs. 3,000 / Quarter", order=2)
            Fees.objects.create(title="Tuition Fee (Secondary)", value="Rs. 4,000 / Quarter", order=3)
            Fees.objects.create(title="Transport Fee", value="Rs. 1,500 / Month (Optional)", order=4)
        self.stdout.write(self.style.SUCCESS('Fees filled.'))

        # 14. Results & Academics
        if not ResultsAcademics.objects.exists():
            ResultsAcademics.objects.create(
                title="Class X Results 2024", 
                file=ContentFile(b'dummy_pdf_data', name='class_x_results.pdf'),
                order=1
            )
            ResultsAcademics.objects.create(
                title="Class XII Results 2024", 
                file=ContentFile(b'dummy_pdf_data', name='class_xii_results.pdf'),
                order=2
            )
            ResultsAcademics.objects.create(
                title="List of PTA Members", 
                file=ContentFile(b'dummy_pdf_data', name='pta_members.pdf'),
                order=3
            )
        self.stdout.write(self.style.SUCCESS('Results & Academics filled.'))

        # 15. Admissions
        adm_settings, _ = AdmissionSettings.objects.get_or_create()
        adm_settings.hero_title = "Admissions Open 2025-26"
        adm_settings.hero_subtitle = "Join the Sunrise Family"
        adm_settings.overview_title = "Admission Process"
        adm_settings.overview_content = "Simple 4-step process to secure your child's future."
        # Note: apply_title/description do not exist in model, skipping.
        adm_settings.save()
        
        if not AdmissionStep.objects.exists():
            AdmissionStep.objects.create(title="Registration", description="Fill the online registration form.", order=1)
            AdmissionStep.objects.create(title="Document Verification", description="Submit necessary documents at school office.", order=2)
            AdmissionStep.objects.create(title="Interaction", description="Interaction with child and parents.", order=3)
            AdmissionStep.objects.create(title="Admission Offer", description="Fee payment and admission confirmation.", order=4)
        self.stdout.write(self.style.SUCCESS('Admissions filled.'))

        # 16. Facilities
        if not Facility.objects.exists():
            Facility.objects.create(
                name="Smart Classrooms",
                short_description="Equipped with digital boards and projectors.",
                icon="computer",
                cover_image=ContentFile(b'dummy_image_data', name='classroom.jpg')
            )
            Facility.objects.create(
                name="Sports Complex",
                short_description="Football, Cricket, and Athletics tracks.",
                icon="trophy",
                cover_image=ContentFile(b'dummy_image_data', name='sports.jpg')
            )
            Facility.objects.create(
                name="Library",
                short_description="Thousands of books for all ages.",
                icon="book",
                cover_image=ContentFile(b'dummy_image_data', name='library.jpg')
            )
        self.stdout.write(self.style.SUCCESS('Facilities filled.'))

        # 17. Gallery
        if not GalleryCategory.objects.exists():
            cat1 = GalleryCategory.objects.create(name="Annual Function")
            cat2 = GalleryCategory.objects.create(name="Sports")
            
            GalleryImage.objects.create(title="Dance Performance", category=cat1, image=ContentFile(b'dummy_image_data', name='dance.jpg'))
            GalleryImage.objects.create(title="Chief Guest Speech", category=cat1, image=ContentFile(b'dummy_image_data', name='speech.jpg'))
            GalleryImage.objects.create(title="Relay Race", category=cat2, image=ContentFile(b'dummy_image_data', name='race.jpg'))
        self.stdout.write(self.style.SUCCESS('Gallery filled.'))

        # 18. Testimonials
        if not Testimonial.objects.exists():
            Testimonial.objects.create(
                name="Priya Singh",
                role="Parent",
                content="Excellent school with caring teachers. My child loves going to school every day.",
                rating=5,
                is_active=True
            )
            Testimonial.objects.create(
                name="Rahul Verma",
                role="Alumni",
                content="Sunrise Public School gave me the foundation to succeed in my career. Forever grateful.",
                rating=5,
                is_active=True
            )
        self.stdout.write(self.style.SUCCESS('Testimonials filled.'))

        # 19. Achievements
        if not Achievement.objects.exists():
            Achievement.objects.create(
                title="Best School Award 2024",
                year="2024",
                description="Awarded by the State Education Board for excellence.",
                image=ContentFile(b'dummy_image_data', name='award.jpg')
            )
            Achievement.objects.create(
                title="National Science Olympiad Winner",
                year="2024",
                description="Our student Rohan Kumar secured 1st rank nationally.",
                image=ContentFile(b'dummy_image_data', name='winner.jpg')
            )
        self.stdout.write(self.style.SUCCESS('Achievements filled.'))

        # 20. About Page Details (Management & Timeline)
        if not ManagementMember.objects.exists():
            ManagementMember.objects.create(name="Mr. A. K. Gupta", position="Chairman", bio="Founder of the trust.", order=1)
            ManagementMember.objects.create(name="Mrs. S. Gupta", position="Director", bio="Visionary leader.", order=2)

        if not TimelineEvent.objects.exists():
            TimelineEvent.objects.create(year="1995", title="Foundation", description="School founded with 50 students.", order=1)
            TimelineEvent.objects.create(year="2005", title="New Campus", description="Shifted to 10-acre campus.", order=2)
            TimelineEvent.objects.create(year="2015", title="Silver Jubilee", description="Celebrated 25 years of excellence.", order=3)
        self.stdout.write(self.style.SUCCESS('About Details filled.'))

        # 21. Quick Links
        if not QuickLink.objects.exists():
            QuickLink.objects.create(title="Admissions", url="/admissions", order=1)
            QuickLink.objects.create(title="Contact Us", url="/contact", order=2)
            QuickLink.objects.create(title="Gallery", url="/gallery", order=3)
            QuickLink.objects.create(title="Alumni", url="/alumni", order=4)
        self.stdout.write(self.style.SUCCESS('Quick Links filled.'))
        
        self.stdout.write(self.style.SUCCESS('SUCCESS: All dummy data populated successfully.'))
