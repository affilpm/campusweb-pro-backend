
import os
import django
import sys

# Add the project root to the python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.school_info.models import (
    ResultsAcademics, Infrastructure, GeneralInfo, Fees, Documentation
)

def create_dummy_data():
    print("Creating dummy data...")

    # Results & Academics
    if not ResultsAcademics.objects.exists():
        print("Adding ResultsAcademics...")
        ResultsAcademics.objects.create(
            title="Class X Board Results 2024",
            value="100% Pass Rate with 50% Distinctions",
            order=1
        )
        ResultsAcademics.objects.create(
            title="Class XII Board Results 2024",
            value="98% Pass Rate. School Topper: 99.2%",
            order=2
        )
        ResultsAcademics.objects.create(
            title="Annual Sports Meet Report",
            value="Overall Championship won by Red House",
            order=3
        )

    # Infrastructure
    if not Infrastructure.objects.exists():
        print("Adding Infrastructure...")
        Infrastructure.objects.create(title="Total Campus Area", value="5 Acres", order=1)
        Infrastructure.objects.create(title="Classrooms", value="45 Smart Classrooms", order=2)
        Infrastructure.objects.create(title="Laboratories", value="Physics, Chemistry, Biology, Computer, Math", order=3)
        Infrastructure.objects.create(title="Library", value="Stocked with 10,000+ books and digital resources", order=4)
        Infrastructure.objects.create(title="Sports Facilities", value="Football ground, Basketball court, Indoor games hall", order=5)

    # General Info
    if not GeneralInfo.objects.exists():
        print("Adding General Info...")
        GeneralInfo.objects.create(title="School Code", value="SC-2023-001", order=1)
        GeneralInfo.objects.create(title="Affiliation Number", value="CBSE/AFF/12345/2023", order=2)
        GeneralInfo.objects.create(title="Principal Name", value="Dr. Sarah Johnson", order=3)
        GeneralInfo.objects.create(title="Contact Email", value="info@schoolexample.com", order=4)

    # Fees
    if not Fees.objects.exists():
        print("Adding Fees...")
        Fees.objects.create(title="Admission Fee", value="₹ 25,000 (One-time, Non-refundable)", order=1)
        Fees.objects.create(title="Tuition Fee (Primary)", value="₹ 45,000 per annum", order=2)
        Fees.objects.create(title="Tuition Fee (Secondary)", value="₹ 55,000 per annum", order=3)
        Fees.objects.create(title="Transport Fee", value="₹ 15,000 - ₹ 20,000 per annum (varies by distance)", order=4)

    # Documentation
    if not Documentation.objects.exists():
        print("Adding Documentation...")
        Documentation.objects.create(title="School Safety Certificate", description="Valid until Dec 2025", order=1)
        Documentation.objects.create(title="Water & Sanitation Certificate", description="Certified by Municipal Corporation", order=2)

    print("Dummy data creation complete.")

if __name__ == '__main__':
    create_dummy_data()
