from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from portal.models import Camp, VolunteerProfile, CampApplication, Testimonial
from datetime import timedelta
import random

class Command(BaseCommand):
    """
    Django management command to populate the database with sample data.
    This command creates a default admin user and sample data for
    camps, volunteers, applications, and testimonials for demonstration purposes.
    """
    help = 'Populates the database with sample data for the Eco Volunteers project'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting database population...'))
        
        # Create superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123', 
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write(self.style.SUCCESS('Admin superuser created'))
        else:
            admin_user = User.objects.get(username='admin')
            self.stdout.write(self.style.SUCCESS('Admin superuser already exists'))
            
        # Create some regular users for volunteers
        volunteer_data = [
            {'username': 'maria', 'email': 'maria@example.com', 'password': 'password123', 
             'first_name': 'Maria', 'last_name': 'Garcia', 'profile': {
                 'phone': '555-123-4567', 'address': '123 Main St, Springfield',
                 'date_of_birth': timezone.now().date() - timedelta(days=365*25),
                 'gender': 'F', 'skills': 'Wildlife monitoring, bird watching, plant identification',
                 'experience': '2 years volunteering with wildlife sanctuary'
             }},
            {'username': 'john', 'email': 'john@example.com', 'password': 'password123', 
             'first_name': 'John', 'last_name': 'Smith', 'profile': {
                 'phone': '555-987-6543', 'address': '456 Oak Ave, Riverside',
                 'date_of_birth': timezone.now().date() - timedelta(days=365*30),
                 'gender': 'M', 'skills': 'First aid, carpentry, trail maintenance',
                 'experience': 'Led 3 conservation projects in national parks'
             }},
            {'username': 'amina', 'email': 'amina@example.com', 'password': 'password123', 
             'first_name': 'Amina', 'last_name': 'Khan', 'profile': {
                 'phone': '555-456-7890', 'address': '789 Pine St, Lakeside',
                 'date_of_birth': timezone.now().date() - timedelta(days=365*22),
                 'gender': 'F', 'skills': 'Marine biology, scuba diving, data collection',
                 'experience': 'Marine biology student with coral reef restoration experience'
             }},
            {'username': 'carlos', 'email': 'carlos@example.com', 'password': 'password123', 
             'first_name': 'Carlos', 'last_name': 'Rodriguez', 'profile': {
                 'phone': '555-321-9876', 'address': '234 Maple Dr, Hillside',
                 'date_of_birth': timezone.now().date() - timedelta(days=365*28),
                 'gender': 'M', 'skills': 'Photography, social media, community outreach',
                 'experience': 'Environmental journalist and social media manager'
             }},
        ]
        
        volunteer_users = []
        for data in volunteer_data:
            profile_data = data.pop('profile')
            if not User.objects.filter(username=data['username']).exists():
                user = User.objects.create_user(**data)
                VolunteerProfile.objects.create(user=user, **profile_data)
                volunteer_users.append(user)
                self.stdout.write(self.style.SUCCESS(f'Created volunteer: {user.username}'))
            else:
                user = User.objects.get(username=data['username'])
                volunteer_users.append(user)
                self.stdout.write(self.style.SUCCESS(f'Volunteer already exists: {user.username}'))
                
        # Create sample environmental camps
        camp_data = [
            {
                'name': 'Amazon Rainforest Conservation',
                'location': 'Brazil, Amazon Basin',
                'description': 'Join our efforts to protect and restore the Amazon rainforest. '
                               'Activities include tree planting, wildlife monitoring, and working '
                               'with local communities on sustainable practices.',
                'start_date': timezone.now().date() + timedelta(days=30),
                'end_date': timezone.now().date() + timedelta(days=44),
                'max_volunteers': 15,
                'is_active': True
            },
            {
                'name': 'Coral Reef Restoration',
                'location': 'Great Barrier Reef, Australia',
                'description': 'Help restore damaged coral reefs through coral planting, '
                               'water quality monitoring, and beach clean-up activities. '
                               'Scuba certification beneficial but not required.',
                'start_date': timezone.now().date() + timedelta(days=60),
                'end_date': timezone.now().date() + timedelta(days=74),
                'max_volunteers': 12,
                'is_active': True
            },
            {
                'name': 'Alpine Ecosystem Protection',
                'location': 'Rocky Mountains, USA',
                'description': 'Work on trail maintenance, erosion control, and alpine habitat '
                               'restoration in one of America\'s most beautiful mountain ranges. '
                               'Physical fitness required for high altitude work.',
                'start_date': timezone.now().date() + timedelta(days=45),
                'end_date': timezone.now().date() + timedelta(days=52),
                'max_volunteers': 20,
                'is_active': True
            },
            {
                'name': 'Marine Conservation Expedition',
                'location': 'Bali, Indonesia',
                'description': 'Participate in marine biodiversity surveys, sea turtle protection, '
                               'and community education programs on this beautiful Indonesian island. '
                               'Learn about marine ecosystems while making a difference.',
                'start_date': timezone.now().date() + timedelta(days=90),
                'end_date': timezone.now().date() + timedelta(days=104),
                'max_volunteers': 18,
                'is_active': True
            },
            {
                'name': 'Urban Wildlife Habitat Creation',
                'location': 'Berlin, Germany',
                'description': 'Help transform urban spaces into wildlife-friendly habitats. '
                               'Projects include building bird and bat houses, creating urban '
                               'gardens, and conducting city wildlife surveys.',
                'start_date': timezone.now().date() + timedelta(days=20),
                'end_date': timezone.now().date() + timedelta(days=26),
                'max_volunteers': 25,
                'is_active': True
            },
        ]
        
        camps = []
        for data in camp_data:
            if not Camp.objects.filter(name=data['name']).exists():
                camp = Camp.objects.create(**data)
                camps.append(camp)
                self.stdout.write(self.style.SUCCESS(f'Created camp: {camp.name}'))
            else:
                camp = Camp.objects.get(name=data['name'])
                camps.append(camp)
                self.stdout.write(self.style.SUCCESS(f'Camp already exists: {camp.name}'))
                
        # Create camp applications with different statuses
        statuses = ['PENDING', 'APPROVED', 'REJECTED', 'WAITLISTED']
        for user in volunteer_users:
            # Each user applies to 1-3 random camps
            applied_camps = random.sample(camps, random.randint(1, min(3, len(camps))))
            for camp in applied_camps:
                if not CampApplication.objects.filter(volunteer=user, camp=camp).exists():
                    status = random.choice(statuses)
                    app = CampApplication.objects.create(
                        volunteer=user,
                        camp=camp,
                        status=status,
                        motivation=f"I'm excited to join the {camp.name} camp because I want to make a "
                                   f"difference and learn more about environmental conservation.",
                        dietary_restrictions=random.choice([
                            'Vegetarian', 'No restrictions', 'Vegan', 'No seafood', ''
                        ]),
                        medical_conditions=random.choice([
                            'None', 'Mild asthma', 'Allergies to certain plants', ''
                        ]),
                        admin_notes=f"User contacted on {timezone.now().date() - timedelta(days=3)}" if status != 'PENDING' else ""
                    )
                    self.stdout.write(self.style.SUCCESS(
                        f'Created application: {user.username} -> {camp.name} ({status})'
                    ))
                else:
                    self.stdout.write(self.style.SUCCESS(
                        f'Application already exists: {user.username} -> {camp.name}'
                    ))
                    
        # Create testimonials for approved applications
        approved_apps = CampApplication.objects.filter(status='APPROVED')
        for app in approved_apps:
            if not Testimonial.objects.filter(volunteer=app.volunteer, camp=app.camp).exists():
                is_approved = random.choice([True, False])
                testimonial = Testimonial.objects.create(
                    volunteer=app.volunteer,
                    camp=app.camp,
                    content=f"My experience at {app.camp.name} was transformative. "
                           f"I learned so much about {app.camp.name.split()[0]} conservation and made "
                           f"lifelong friends. The staff was knowledgeable and supportive.",
                    rating=random.randint(3, 5),
                    is_approved=is_approved
                )
                self.stdout.write(self.style.SUCCESS(
                    f'Created testimonial: {app.volunteer.username} -> {app.camp.name} '
                    f'({"Approved" if is_approved else "Pending"})'
                ))
            else:
                self.stdout.write(self.style.SUCCESS(
                    f'Testimonial already exists: {app.volunteer.username} -> {app.camp.name}'
                ))
                
        self.stdout.write(self.style.SUCCESS('Database successfully populated with sample data!'))
        self.stdout.write(self.style.SUCCESS('\nAdmin access:'))
        self.stdout.write(self.style.SUCCESS('Username: admin'))
        self.stdout.write(self.style.SUCCESS('Password: admin123'))
        self.stdout.write(self.style.SUCCESS('\nSample volunteer access:'))
        self.stdout.write(self.style.SUCCESS('Username: maria (or john, amina, carlos)'))
        self.stdout.write(self.style.SUCCESS('Password: password123'))