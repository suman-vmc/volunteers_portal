"""
URL configuration for eco_volunteers project.

This is the main URL configuration file for the entire project.
It includes URLs from Django's admin site and our custom portal app.

Django URL patterns are processed from top to bottom, so order matters.
Each path() function maps a URL pattern to a view function or included URLconf.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django's built-in admin panel
    # Accessible at /admin/ and requires superuser authentication
    path('admin/', admin.site.urls),  
    
    # Our main app's URLs defined in portal/urls.py
    # The empty string means these URLs have no prefix
    path('', include('portal.urls')),  
]

# Serve media files (like uploaded images) in development
# In production, these should be served by a web server like Nginx
if settings.DEBUG:
    # This configuration allows accessing user-uploaded files during development
    # Example: camp images will be accessible at /media/camp_images/filename.jpg
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
