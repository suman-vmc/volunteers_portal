# Eco Volunteers - Environmental Volunteering Portal

## Project Overview

 This is my final year project on Eco Volunteers portal and this is a comprehensive Django-based web application designed to connect environmental volunteers with conservation camps and opportunities. The platform serves as a bridge between environmental NGOs that organize conservation camps and volunteers who want to contribute to ecological causes.

## Features

### For Volunteers
- **User Registration & Authentication**: Create accounts with detailed profiles
- **Camp Discovery**: Browse and search for environmental conservation camps
- **Application Management**: Apply to join camps and track application status
- **Interactive Profiles**: Manage personal information and volunteering history
- **Testimonials & Feedback**: Share experiences after participating in camps

### For Administrators
- **Comprehensive Dashboard**: View key statistics and insights at a glance
- **Camp Management**: Create, edit, activate/deactivate, and delete camps
- **Volunteer Management**: Review volunteer profiles and application history
- **Application Processing**: Approve, reject, or waitlist volunteer applications
- **Testimonial Moderation**: Review and approve volunteer testimonials
- **Advanced Filtering**: Sort and filter data for better management

## Technology Stack

- **Backend Framework**: Django 4.2+ (Python)
- **Database**: SQLite (default), compatible with PostgreSQL for production
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **CSS Framework**: Bootstrap 5 for responsive design
- **Icons**: Font Awesome for high-quality icon set
- **Image Handling**: Pillow for image processing
- **Form Handling**: Django Forms with custom validation
- **Authentication**: Django's built-in authentication system with custom extensions
- **Admin Interface**: Custom Django admin and dedicated admin portal

## Project Structure

```
eco_volunteers/
├── eco_volunteers/        # Project settings and configuration
│   ├── settings.py        # Django settings for the project
│   ├── urls.py            # Main URL routing
│   ├── wsgi.py & asgi.py  # Web server configuration
│
├── portal/                # Main application directory
│   ├── admin.py           # Django admin configuration
│   ├── forms.py           # Form definitions for user input
│   ├── models.py          # Database models
│   ├── urls.py            # URL routing for the portal app
│   ├── views.py           # View functions that handle requests
│   ├── migrations/        # Database migrations
│   ├── tests.py           # Test cases
│
├── templates/             # HTML templates
│   ├── accounts/          # User account templates
│   ├── admin/             # Custom admin templates
│   ├── camps/             # Camp-related templates
│   ├── base.html          # Base template with common elements
│
├── static/                # Static files (CSS, JS, images)
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript files
│   ├── images/            # Static image assets
│
├── media/                 # User-uploaded files (camp images)
├── manage.py              # Django command-line utility
└── README.md              # Project documentation
```

## Installation Guide

### Prerequisites
- Python 3.8+ installed on your system
- Basic knowledge of command-line operations
- pip (Python package manager)

### Step 1: Clone or Download the Project
Download the project ZIP file and extract it to your preferred location, or clone from a repository.

### Step 2: Set Up Virtual Environment (Recommended)
A virtual environment helps keep dependencies separate from other projects.

```bash
# Navigate to project directory
cd eco_volunteers

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
# Install required packages
pip install django pillow
```

### Step 4: Initialize the Database
```bash
# Apply migrations to create database structure
python manage.py migrate
```

### Step 5: Create an Admin User
```bash
# Create a superuser account to access admin features
python manage.py createsuperuser
# Follow the prompts to set username, email, and password
```

### Step 6: Run the Development Server
```bash
# Start the Django development server
python manage.py runserver
```

### Step 7: Access the Application
- Open your browser and navigate to: http://127.0.0.1:8000/
- Access the Django admin at: http://127.0.0.1:8000/admin/
- Access the custom admin dashboard at: http://127.0.0.1:8000/admin-dashboard/

## User Guide

### As a Volunteer
1. **Register an Account**: Create an account with your personal information
2. **Complete Your Profile**: Add skills, experience, and emergency contacts
3. **Browse Camps**: Explore active environmental camps
4. **Apply to Camps**: Submit applications with your motivation and requirements
5. **Track Applications**: Monitor the status of your camp applications
6. **Submit Testimonials**: Share your experience after participating in a camp

### As an Administrator
1. **Access Admin Dashboard**: Log in with admin credentials
2. **Manage Camps**: Create new camps, edit details, or delete outdated ones
3. **Review Applications**: Approve or reject volunteer applications
4. **Manage Volunteers**: View volunteer profiles and their application history
5. **Moderate Testimonials**: Review and approve volunteer testimonials
6. **Access Statistics**: View participation rates and other key metrics

## Development Guidelines

### Coding Standards
- Follow PEP 8 for Python code style
- Use meaningful variable and function names
- Include docstrings for all functions and classes
- Keep functions small and focused on a single responsibility

### Database Migrations
When making model changes:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Running Tests
```bash
python manage.py test portal
```

## License and Credits

This project was developed as an Academic project in web application for managing environmental volunteering activities. It is designed for project to demonstrate Django web application development with a focus on user authentication, data management, and administrative functionalities.

## Contact

For any questions or issues regarding this project, please contact the project maintainer .

