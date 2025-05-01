from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Camp, VolunteerProfile, CampApplication
from datetime import date, timedelta


class ModelTests(TestCase):
    """Test cases for models"""
    
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testvolunteer',
            email='test@example.com',
            password='test1234',
            first_name='Test',
            last_name='Volunteer'
        )
        
        # Create test profile
        self.profile = VolunteerProfile.objects.create(
            user=self.user,
            phone='1234567890',
            address='123 Test St',
            date_of_birth=date(1990, 1, 1)
        )
        
        # Create test camp
        self.camp = Camp.objects.create(
            name='Test Camp',
            location='Test Location',
            description='Test Description',
            start_date=date.today() + timedelta(days=30),
            end_date=date.today() + timedelta(days=35),
            max_volunteers=20
        )
    
    def test_camp_str(self):
        """Test Camp string representation"""
        self.assertEqual(str(self.camp), 'Test Camp')
    
    def test_volunteer_profile_str(self):
        """Test VolunteerProfile string representation"""
        self.assertEqual(str(self.profile), "Test Volunteer's Profile")
    
    def test_days_until_start(self):
        """Test days until camp start calculation"""
        self.assertEqual(self.camp.days_until_start(), 30)
    
    def test_volunteer_age(self):
        """Test volunteer age calculation"""
        # This may need adjustment based on test date
        expected_age = date.today().year - 1990
        if (date.today().month, date.today().day) < (1, 1):
            expected_age -= 1
        self.assertEqual(self.profile.age(), expected_age)


class ViewTests(TestCase):
    """Test cases for views"""
    
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testvolunteer',
            email='test@example.com',
            password='test1234'
        )
        
        # Create admin user
        self.admin_user = User.objects.create_user(
            username='testadmin',
            email='admin@example.com',
            password='admin1234',
            is_staff=True
        )
        
        # Create test camp
        self.camp = Camp.objects.create(
            name='Test Camp',
            location='Test Location',
            description='Test Description',
            start_date=date.today() + timedelta(days=30),
            end_date=date.today() + timedelta(days=35),
            max_volunteers=20
        )
    
    def test_home_view(self):
        """Test home page view"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
    
    def test_camp_list_view(self):
        """Test camp list view"""
        response = self.client.get(reverse('camp_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'camps/camp_list.html')
        self.assertContains(response, 'Test Camp')
    
    def test_camp_detail_view(self):
        """Test camp detail view"""
        response = self.client.get(reverse('camp_detail', args=[self.camp.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'camps/camp_detail.html')
        self.assertContains(response, 'Test Camp')
    
    def test_login_required(self):
        """Test login required for applying to camps"""
        # Attempt to apply without login
        response = self.client.get(reverse('apply_to_camp', args=[self.camp.id]))
        self.assertRedirects(
            response, 
            f'/accounts/login/?next={reverse("apply_to_camp", args=[self.camp.id])}'
        )
        
        # Login and try again
        self.client.login(username='testvolunteer', password='test1234')
        response = self.client.get(reverse('apply_to_camp', args=[self.camp.id]))
        self.assertEqual(response.status_code, 200)
