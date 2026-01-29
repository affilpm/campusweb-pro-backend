"""
Tests for Admin Authentication.
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import AdminUser


class AdminUserModelTest(TestCase):
    """
    Tests for AdminUser model.
    """
    
    def test_create_admin_user(self):
        """Test creating a regular admin user."""
        user = AdminUser.objects.create_user(
            email='admin@school.edu',
            password='TestPass@123',
            first_name='Test',
            last_name='Admin',
        )
        
        self.assertEqual(user.email, 'admin@school.edu')
        self.assertTrue(user.check_password('TestPass@123'))
        self.assertEqual(user.get_full_name(), 'Test Admin')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_create_superuser(self):
        """Test creating a superuser."""
        user = AdminUser.objects.create_superuser(
            email='superadmin@school.edu',
            password='SuperPass@123',
            first_name='Super',
            last_name='Admin',
        )
        
        self.assertEqual(user.email, 'superadmin@school.edu')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertEqual(user.role, AdminUser.Role.SUPER_ADMIN)
    
    def test_email_required(self):
        """Test that email is required."""
        with self.assertRaises(ValueError):
            AdminUser.objects.create_user(
                email='',
                password='TestPass@123',
            )


class AdminLoginTest(APITestCase):
    """
    Tests for Admin Login endpoint.
    """
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.login_url = reverse('authentication:login')
        
        # Create test admin user
        self.admin_user = AdminUser.objects.create_user(
            email='admin@school.edu',
            password='TestPass@123',
            first_name='Test',
            last_name='Admin',
        )
    
    def test_login_success(self):
        """Test successful admin login."""
        response = self.client.post(
            self.login_url,
            {
                'email': 'admin@school.edu',
                'password': 'TestPass@123',
            },
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertIn('access', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['email'], 'admin@school.edu')
        
        # Check refresh token cookie is set
        self.assertIn('refresh_token', response.cookies)
    
    def test_login_invalid_email(self):
        """Test login with invalid email."""
        response = self.client.post(
            self.login_url,
            {
                'email': 'wrong@school.edu',
                'password': 'TestPass@123',
            },
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(response.data['success'])
    
    def test_login_invalid_password(self):
        """Test login with invalid password."""
        response = self.client.post(
            self.login_url,
            {
                'email': 'admin@school.edu',
                'password': 'WrongPassword',
            },
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(response.data['success'])
    
    def test_login_missing_email(self):
        """Test login with missing email."""
        response = self.client.post(
            self.login_url,
            {
                'password': 'TestPass@123',
            },
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_login_missing_password(self):
        """Test login with missing password."""
        response = self.client.post(
            self.login_url,
            {
                'email': 'admin@school.edu',
            },
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_login_inactive_user(self):
        """Test login with inactive user."""
        self.admin_user.is_active = False
        self.admin_user.save()
        
        response = self.client.post(
            self.login_url,
            {
                'email': 'admin@school.edu',
                'password': 'TestPass@123',
            },
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AdminMeTest(APITestCase):
    """
    Tests for Admin Me endpoint.
    """
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.me_url = reverse('authentication:me')
        
        self.admin_user = AdminUser.objects.create_user(
            email='admin@school.edu',
            password='TestPass@123',
            first_name='Test',
            last_name='Admin',
        )
    
    def test_me_authenticated(self):
        """Test getting current user when authenticated."""
        # First login to get the token
        login_response = self.client.post(
            reverse('authentication:login'),
            {
                'email': 'admin@school.edu',
                'password': 'TestPass@123',
            },
            format='json'
        )
        
        access_token = login_response.data['access']
        
        # Use the token to access /me
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.me_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['user']['email'], 'admin@school.edu')
    
    def test_me_unauthenticated(self):
        """Test getting current user when not authenticated."""
        response = self.client.get(self.me_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AdminLogoutTest(APITestCase):
    """
    Tests for Admin Logout endpoint.
    """
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.logout_url = reverse('authentication:logout')
        
        self.admin_user = AdminUser.objects.create_user(
            email='admin@school.edu',
            password='TestPass@123',
            first_name='Test',
            last_name='Admin',
        )
    
    def test_logout_success(self):
        """Test successful logout."""
        # First login
        login_response = self.client.post(
            reverse('authentication:login'),
            {
                'email': 'admin@school.edu',
                'password': 'TestPass@123',
            },
            format='json'
        )
        
        access_token = login_response.data['access']
        
        # Set the cookie and auth header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.client.cookies = login_response.cookies
        
        # Logout
        response = self.client.post(self.logout_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
