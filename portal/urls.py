from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomLoginForm

"""
URL configuration for the eco_volunteers portal app.

This module defines all URL patterns for the environmental volunteering portal,
organized into logical sections for different features of the application.
Each URL pattern is mapped to a specific view function that handles the request 
and generates the appropriate response.
"""

urlpatterns = [
    # Public pages - Accessible to all visitors
    path('', views.home, name='home'),  # Home page with featured camps and testimonials
    path('about/', views.about, name='about'),  # About page with mission and information
    path('contact/', views.contact, name='contact'),  # Contact information page
    
    # Camp listings and details - Camp browsing and application
    path('camps/', views.camp_list, name='camp_list'),  # List all active environmental camps
    path('camps/<int:camp_id>/', views.camp_detail, name='camp_detail'),  # View single camp details
    path('camps/<int:camp_id>/apply/', views.apply_to_camp, name='apply_to_camp'),  # Apply to a specific camp
    
    # Authentication - Login, logout, and registration routes
    # Using Django's built-in auth views with custom templates and forms
    path('accounts/login/', 
         auth_views.LoginView.as_view(
             template_name='accounts/login.html',  # Custom template
             authentication_form=CustomLoginForm  # Custom styled form
         ), 
         name='login'),
    path('accounts/logout/', 
         auth_views.LogoutView.as_view(), 
         name='logout'),
    path('accounts/register/', 
         views.register, 
         name='register'),  # Custom registration with profile creation
    
    # Volunteer profile section - For authenticated volunteers
    path('accounts/profile/', 
         views.profile, 
         name='profile'),  # View and edit volunteer profile
    path('accounts/applications/', 
         views.my_applications, 
         name='my_applications'),  # View user's camp applications and status
    path('accounts/testimonial/', 
         views.add_testimonial, 
         name='add_testimonial'),  # Submit testimonial about camp experience
    
    # Admin dashboard section - Protected by staff permission checks
    path('admin-dashboard/', 
         views.admin_dashboard, 
         name='admin_dashboard'),  # Main admin dashboard with statistics
    
    # Admin Camp Management
    path('admin-dashboard/camps/', 
         views.admin_manage_camps, 
         name='admin_manage_camps'),  # List all camps with management options
    path('admin-dashboard/camps/add/', 
         views.admin_add_camp, 
         name='admin_add_camp'),  # Create new camp form
    path('admin-dashboard/camps/<int:camp_id>/edit/', 
         views.admin_edit_camp, 
         name='admin_edit_camp'),  # Edit existing camp
    path('admin-dashboard/camps/<int:camp_id>/delete/', 
         views.admin_delete_camp, 
         name='admin_delete_camp'),  # Delete camp with confirmation
    
    # Admin Volunteer Management
    path('admin-dashboard/volunteers/', 
         views.admin_manage_volunteers, 
         name='admin_manage_volunteers'),  # View and manage volunteer profiles
    
    # Admin Application Management
    path('admin-dashboard/applications/', 
         views.admin_manage_applications, 
         name='admin_manage_applications'),  # Manage all camp applications
    path('admin-dashboard/applications/<int:application_id>/', 
         views.admin_review_application, 
         name='admin_review_application'),  # Review specific application
    
    # Admin Testimonial Management
    path('admin-dashboard/testimonials/', 
         views.admin_manage_testimonials, 
         name='admin_manage_testimonials'),  # Approve/reject testimonials

     path('logout/', views.logout_view, name='logout'),

]
