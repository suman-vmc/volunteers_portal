from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import login
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout


from .models import Camp, VolunteerProfile, CampApplication, Testimonial
from .forms import (
    CustomUserCreationForm, VolunteerProfileForm, CampApplicationForm,
    CampForm, ApplicationManagementForm, TestimonialForm
)

# Helper functions
def is_admin(user):
    """Check if user is staff"""
    return user.is_staff

# Public views
def home(request):
    """Home page view with featured camps and testimonials"""
    # Get upcoming camps (limited to 3)
    upcoming_camps = Camp.objects.filter(is_active=True).order_by('start_date')[:3]
    
    # Get approved testimonials (limited to 3)
    testimonials = Testimonial.objects.filter(is_approved=True).order_by('-created_at')[:3]
    
    return render(request, 'home.html', {
        'upcoming_camps': upcoming_camps,
        'testimonials': testimonials
    })

def about(request):
    """About page view"""
    return render(request, 'about.html')

def contact(request):
    """Contact page view"""
    return render(request, 'contact.html')

def camp_list(request):
    """View for listing all active camps"""
    camps = Camp.objects.filter(is_active=True).order_by('start_date')
    return render(request, 'camps/camp_list.html', {'camps': camps})

def camp_detail(request, camp_id):
    camp = get_object_or_404(Camp, pk=camp_id)
    approved_testimonials = camp.testimonials.filter(is_approved=True)
    has_approved_testimonials = approved_testimonials.exists()
    spots_left = camp.max_volunteers - camp.get_registered_volunteers_count()

    
    return render(request, 'camps/camp_detail.html', {
        'camp': camp,
        'approved_testimonials': approved_testimonials,
        'has_approved_testimonials': has_approved_testimonials,
        'spots_left': spots_left
    })


# Authentication and profile views
def register(request):
    """
    User registration view that creates both User and VolunteerProfile
    """
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        profile_form = VolunteerProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            # Create but don't save the user instance yet
            user = user_form.save()
            
            # Save the profile
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            
            # Log the user in
            login(request, user)
            messages.success(request, "Registration successful! Welcome to EcoVolunteers.")
            return redirect('home')
    else:
        user_form = CustomUserCreationForm()
        profile_form = VolunteerProfileForm()
    
    return render(request, 'accounts/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def profile(request):
    """
    View for users to see and edit their profile information
    """
    try:
        profile = request.user.profile
    except VolunteerProfile.DoesNotExist:
        # Create profile if it doesn't exist
        profile = VolunteerProfile(user=request.user)
    
    if request.method == 'POST':
        form = VolunteerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('profile')
    else:
        form = VolunteerProfileForm(instance=profile)

    approved_count = request.user.applications.filter(status='APPROVED').count()

    return render(request, 'accounts/profile.html', { 'approved_count': approved_count, 'form': form})

    """
    View for users to see their camp applications
    """
@login_required
def my_applications(request):
    """
    View for users to see their camp applications
    """
    applications = CampApplication.objects.filter(
        volunteer=request.user
    ).select_related('camp').order_by('-created_at')
    
    return render(request, 'accounts/applications.html', {
        'applications': applications
    })

@login_required
def apply_to_camp(request, camp_id):
    """
    View for users to apply to a specific camp
    """
    camp = get_object_or_404(Camp, pk=camp_id)
    
    # Check if user has already applied
    existing_application = CampApplication.objects.filter(
        volunteer=request.user,
        camp=camp
    ).first()
    
    if existing_application:
        messages.info(request, f"You have already applied to {camp.name}.")
        return redirect('camp_detail', camp_id=camp.id)
    
    # Check if camp is full
    if not camp.is_registration_open():
        messages.error(request, "Sorry, this camp is either full or not accepting applications.")
        return redirect('camp_detail', camp_id=camp.id)
    
    if request.method == 'POST':
        form = CampApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.volunteer = request.user
            application.camp = camp
            application.save()
            
            messages.success(request, f"Your application to {camp.name} has been submitted successfully!")
            return redirect('my_applications')
    else:
        form = CampApplicationForm()
    
    return render(request, 'camps/apply.html', {
        'form': form,
        'camp': camp
    })

@login_required
def add_testimonial(request):
    """
    View for volunteers to submit testimonials about camps
    """
    # Check if the user has any approved applications
    has_approved_applications = CampApplication.objects.filter(
        volunteer=request.user,
        status='APPROVED'
    ).exists()
    
    if not has_approved_applications:
        messages.info(request, "You need to participate in a camp before submitting a testimonial.")
        return redirect('profile')
    
    if request.method == 'POST':
        form = TestimonialForm(request.POST, user=request.user)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.volunteer = request.user
            testimonial.save()
            
            messages.success(request, "Thank you for your testimonial! It will be reviewed by our admins.")
            return redirect('profile')
    else:
        form = TestimonialForm(user=request.user)
    
    return render(request, 'accounts/add_testimonial.html', {'form': form})

# Admin dashboard views
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """
    Main admin dashboard view with statistics
    """
    # Count total camps
    total_camps = Camp.objects.count()
    active_camps = Camp.objects.filter(is_active=True).count()
    
    # Count volunteers
    total_volunteers = VolunteerProfile.objects.count()
    
    # Count applications by status
    applications = CampApplication.objects.all()
    pending_applications = applications.filter(status='PENDING').count()
    approved_applications = applications.filter(status='APPROVED').count()
    
    # Get camps with the most applications
    popular_camps = Camp.objects.annotate(
        application_count=Count('applications')
    ).order_by('-application_count')[:5]
    
    return render(request, 'admin/dashboard.html', {
        'total_camps': total_camps,
        'active_camps': active_camps,
        'total_volunteers': total_volunteers,
        'pending_applications': pending_applications,
        'approved_applications': approved_applications,
        'popular_camps': popular_camps,
    })

@login_required
@user_passes_test(is_admin)
def admin_manage_camps(request):
    """
    Admin view for managing all camps
    """
    camps = Camp.objects.all().order_by('-created_at')
    return render(request, 'admin/manage_camps.html', {'camps': camps})

@login_required
@user_passes_test(is_admin)
def admin_add_camp(request):
    """
    Admin view for adding a new camp
    """
    if request.method == 'POST':
        form = CampForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "New camp created successfully!")
            return redirect('admin_manage_camps')
    else:
        form = CampForm()
    
    return render(request, 'admin/camp_form.html', {
        'form': form,
        'title': 'Add New Camp',
        'button_text': 'Create Camp'
    })

@login_required
@user_passes_test(is_admin)
def admin_edit_camp(request, camp_id):
    """
    Admin view for editing an existing camp
    """
    camp = get_object_or_404(Camp, pk=camp_id)
    
    if request.method == 'POST':
        form = CampForm(request.POST, request.FILES, instance=camp)
        if form.is_valid():
            form.save()
            messages.success(request, f"{camp.name} updated successfully!")
            return redirect('admin_manage_camps')
    else:
        form = CampForm(instance=camp)
    
    return render(request, 'admin/camp_form.html', {
        'form': form,
        'camp': camp,
        'title': f'Edit Camp: {camp.name}',
        'button_text': 'Update Camp'
    })

@login_required
@user_passes_test(is_admin)
def admin_delete_camp(request, camp_id):
    """
    Admin view for deleting a camp
    """
    camp = get_object_or_404(Camp, pk=camp_id)
    
    if request.method == 'POST':
        camp_name = camp.name
        camp.delete()
        messages.success(request, f"{camp_name} has been deleted.")
        return redirect('admin_manage_camps')
    
    return render(request, 'admin/confirm_delete.html', {
        'camp': camp,
        'title': f'Delete Camp: {camp.name}'
    })

@login_required
@user_passes_test(is_admin)
def admin_manage_volunteers(request):
    """
    Admin view for managing all volunteers
    """
    volunteers = VolunteerProfile.objects.select_related('user').all()
    return render(request, 'admin/manage_volunteers.html', {'volunteers': volunteers})

@login_required
@user_passes_test(is_admin)
def admin_manage_applications(request):
    """
    Admin view for managing all camp applications
    """
    # Get filter parameters
    status = request.GET.get('status', '')
    camp_id = request.GET.get('camp', '')
    
    # Start with all applications
    applications = CampApplication.objects.select_related('volunteer', 'camp').all()
    
    # Apply filters if provided
    if status:
        applications = applications.filter(status=status)
    if camp_id:
        applications = applications.filter(camp_id=camp_id)
    
    # Get camps for filter dropdown
    camps = Camp.objects.all()
    
    return render(request, 'admin/applications.html', {
        'applications': applications,
        'camps': camps,
        'current_status': status,
        'current_camp': camp_id
    })

@login_required
@user_passes_test(is_admin)
def admin_review_application(request, application_id):
    """
    Admin view for reviewing a specific application
    """
    application = get_object_or_404(CampApplication, pk=application_id)
    
    if request.method == 'POST':
        form = ApplicationManagementForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, f"Application updated successfully.")
            return redirect('admin_manage_applications')
    else:
        form = ApplicationManagementForm(instance=application)
    
    return render(request, 'admin/review_application.html', {
        'form': form,
        'application': application
    })

@login_required
@user_passes_test(is_admin)
def admin_manage_testimonials(request):
    """
    Admin view for managing testimonials
    """
    testimonials = Testimonial.objects.select_related('volunteer', 'camp').all().order_by('-created_at')
    
    # Handle approval/rejection
    if request.method == 'POST':
        testimonial_id = request.POST.get('testimonial_id')
        action = request.POST.get('action')
        
        if testimonial_id and action:
            testimonial = get_object_or_404(Testimonial, pk=testimonial_id)
            
            if action == 'approve':
                testimonial.is_approved = True
                testimonial.save()
                messages.success(request, "Testimonial approved.")
            elif action == 'reject':
                testimonial.is_approved = False
                testimonial.save()
                messages.success(request, "Testimonial rejected.")
    
    return render(request, 'admin/testimonials.html', {'testimonials': testimonials})

def logout_view(request):
    logout(request)
    return redirect('home')