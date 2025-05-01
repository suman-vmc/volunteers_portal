from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Camp(models.Model):
    """
    Model for environmental camps that volunteers can register for
    """
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    max_volunteers = models.PositiveIntegerField(default=20)
    image = models.ImageField(upload_to='camp_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def days_until_start(self):
        """Calculate days until camp starts"""
        today = timezone.now().date()
        return (self.start_date - today).days
    
    def get_registered_volunteers_count(self):
        """Get number of registered volunteers"""
        return self.applications.filter(status='APPROVED').count()
    
    def is_registration_open(self):
        """Check if registration is still open"""
        return self.is_active and self.get_registered_volunteers_count() < self.max_volunteers


class VolunteerProfile(models.Model):
    """
    Extended profile for volunteers with additional information
    """
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15)
    address = models.TextField()
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    emergency_contact = models.CharField(max_length=100, blank=True)
    emergency_phone = models.CharField(max_length=15, blank=True)
    skills = models.TextField(blank=True, help_text="List your skills relevant to environmental volunteering")
    experience = models.TextField(blank=True, help_text="Brief description of your previous volunteer experience")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}'s Profile"
    
    def age(self):
        """Calculate volunteer's age"""
        if self.date_of_birth:
            today = timezone.now().date()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None


class CampApplication(models.Model):
    """
    Model for volunteer applications to specific camps
    """
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('WAITLISTED', 'Waitlisted'),
    ]

    volunteer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    camp = models.ForeignKey(Camp, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    motivation = models.TextField(help_text="Why do you want to join this camp?")
    dietary_restrictions = models.TextField(blank=True, help_text="Any dietary restrictions or allergies")
    medical_conditions = models.TextField(blank=True, help_text="Any medical conditions we should be aware of")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_notes = models.TextField(blank=True, help_text="Admin notes (not visible to volunteer)")

    class Meta:
        unique_together = ('volunteer', 'camp')
        
    def __str__(self):
        return f"{self.volunteer.username}'s application for {self.camp.name}"


class Testimonial(models.Model):
    """
    Model for volunteer testimonials about their camp experiences
    """
    volunteer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='testimonials')
    camp = models.ForeignKey(Camp, on_delete=models.CASCADE, related_name='testimonials', null=True, blank=True)
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5, help_text="Rating out of 5")
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Testimonial by {self.volunteer.username}"
