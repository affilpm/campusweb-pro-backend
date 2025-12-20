"""
Management command to create a default admin user.
"""

from django.core.management.base import BaseCommand
from authentication.models import AdminUser


import os

class Command(BaseCommand):
    help = 'Create a default admin user for development'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            default=os.getenv('DEFAULT_ADMIN_EMAIL', 'admin@example.com'),
            help='Admin email address',
        )
        parser.add_argument(
            '--password',
            default=os.getenv('DEFAULT_ADMIN_PASSWORD', 'admin'),
            help='Admin password',
        )
        parser.add_argument(
            '--first-name',
            default='System',
            help='Admin first name',
        )
        parser.add_argument(
            '--last-name',
            default='Administrator',
            help='Admin last name',
        )

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']
        first_name = options['first_name']
        last_name = options['last_name']

        # Check if user already exists
        if AdminUser.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING(f'Admin user with email {email} already exists.')
            )
            return

        # Create the admin user
        user = AdminUser.objects.create_superuser(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created admin user: {email}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Password: {password}')
        )
