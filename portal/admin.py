from django.contrib import admin
from .models import Camp, VolunteerProfile, CampApplication, Testimonial

"""
Django Admin Configuration for the Eco Volunteers Portal

This module defines the admin interface for the portal's models,
customizing how each model is displayed and managed in the Django admin site.

The admin site provides a powerful interface for site administrators to:
- View, add, edit, and delete records
- Filter and search through data
- Perform batch operations

Each model's admin class customizes:
- Which fields are displayed in the list view (list_display)
- Which fields can be used for filtering (list_filter)
- Which fields can be searched (search_fields)
- Custom methods for computed fields
- And more...
"""

@admin.register(Camp)
class CampAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Camp model
    
    This class defines how environmental camps are displayed and managed
    in the Django admin interface. It includes customizations for:
    - Which fields are shown in the list display
    - Filtering options
    - Search capabilities
    - Date-based navigation
    """
    # Fields shown in the camps list
    list_display = ('name', 'location', 'start_date', 'end_date', 'is_active', 'get_registered_volunteers_count')
    
    # Filters shown in the right sidebar
    list_filter = ('is_active', 'start_date')
    
    # Fields that can be searched via the search box
    search_fields = ('name', 'location', 'description')
    
    # Hierarchical date-based navigation
    date_hierarchy = 'start_date'
    
    def get_registered_volunteers_count(self, obj):
        """
        Custom computed field that displays the number of approved volunteers
        for each camp in the admin list view
        """
        return obj.get_registered_volunteers_count()
    
    # Custom column name in the admin interface
    get_registered_volunteers_count.short_description = 'Registered Volunteers'


@admin.register(VolunteerProfile)
class VolunteerProfileAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the VolunteerProfile model
    
    This class defines how volunteer profiles are displayed and managed
    in the Django admin interface, making it easier to view and
    edit volunteer information.
    """
    # Fields shown in the volunteer list
    list_display = ('user', 'phone', 'gender', 'age')
    
    # Filters shown in the right sidebar
    list_filter = ('gender',)
    
    # Fields that can be searched, including related User model fields
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'phone')
    
    # Use a search widget for the user field (helpful for many users)
    raw_id_fields = ('user',)


@admin.register(CampApplication)
class CampApplicationAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the CampApplication model
    
    This class customizes how volunteer applications are managed,
    allowing administrators to review and update application statuses
    efficiently through the admin interface.
    """
    # Fields shown in the applications list
    list_display = ('volunteer', 'camp', 'status', 'created_at')
    
    # Filters shown in the right sidebar
    list_filter = ('status', 'created_at')
    
    # Fields that can be searched
    search_fields = ('volunteer__username', 'volunteer__email', 'camp__name')
    
    # Hierarchical date-based navigation
    date_hierarchy = 'created_at'
    
    # Use search widgets for these foreign keys
    raw_id_fields = ('volunteer', 'camp')
    
    # Fields that can be edited directly from the list view
    list_editable = ('status',)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Testimonial model
    
    This class customizes the testimonial management interface,
    making it easy for administrators to review, approve, or reject
    testimonials submitted by volunteers.
    """
    # Fields shown in the testimonials list
    list_display = ('volunteer', 'camp', 'rating', 'is_approved', 'created_at')
    
    # Filters shown in the right sidebar
    list_filter = ('is_approved', 'rating', 'created_at')
    
    # Fields that can be searched
    search_fields = ('volunteer__username', 'content', 'camp__name')
    
    # Fields that can be edited directly from the list view
    list_editable = ('is_approved',)
    
    # Use search widgets for these foreign keys
    raw_id_fields = ('volunteer', 'camp')
