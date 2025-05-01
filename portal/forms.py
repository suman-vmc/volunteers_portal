from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import VolunteerProfile, CampApplication, Camp, Testimonial

class CustomUserCreationForm(UserCreationForm):
    """
    Extended user registration form with additional fields
    """
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'


class VolunteerProfileForm(forms.ModelForm):
    """
    Form for volunteer profile information
    """
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
    
    class Meta:
        model = VolunteerProfile
        fields = ('phone', 'address', 'date_of_birth', 'gender', 
                 'emergency_contact', 'emergency_phone', 'skills', 'experience')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'


class CustomLoginForm(AuthenticationForm):
    """
    Custom login form with styled fields
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'


class CampApplicationForm(forms.ModelForm):
    """
    Form for volunteers to apply to camps
    """
    class Meta:
        model = CampApplication
        fields = ('motivation', 'dietary_restrictions', 'medical_conditions')
        widgets = {
            'motivation': forms.Textarea(attrs={'rows': 4}),
            'dietary_restrictions': forms.Textarea(attrs={'rows': 3}),
            'medical_conditions': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'


class CampForm(forms.ModelForm):
    """
    Form for admin to create or edit camps
    """
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
    
    class Meta:
        model = Camp
        fields = ('name', 'location', 'description', 'start_date', 
                 'end_date', 'max_volunteers', 'image', 'is_active')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field_name in self.fields:
            if field_name != 'image':
                self.fields[field_name].widget.attrs['class'] = 'form-control'
            else:
                self.fields[field_name].widget.attrs['class'] = 'form-control-file'

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("End date must be after start date.")
        
        return cleaned_data


class ApplicationManagementForm(forms.ModelForm):
    """
    Form for admin to manage camp applications
    """
    class Meta:
        model = CampApplication
        fields = ('status', 'admin_notes')
        widgets = {
            'admin_notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'


class TestimonialForm(forms.ModelForm):
    """
    Form for volunteers to submit testimonials
    """
    class Meta:
        model = Testimonial
        fields = ('camp', 'content', 'rating')
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Add Bootstrap classes to form fields
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'
        
        # Filter camps to only show those the user has participated in
        if user:
            approved_camps = CampApplication.objects.filter(
                volunteer=user, 
                status='APPROVED'
            ).values_list('camp', flat=True)
            self.fields['camp'].queryset = Camp.objects.filter(id__in=approved_camps)
