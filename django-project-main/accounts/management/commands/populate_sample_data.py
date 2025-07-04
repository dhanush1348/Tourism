from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from bookings.models import Tour, Destination, Category
from accounts.models import Wishlist
import random
from datetime import datetime, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with sample data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')

        # Create sample users
        users = []
        for i in range(1, 6):
            user = User.objects.create_user(
                email=f'user{i}@example.com',
                password='password123',
                first_name=f'User{i}',
                last_name='Test',
                phone_number=f'+123456789{i}',
                preferred_currency=random.choice(['USD', 'EUR', 'GBP', 'JPY']),
                preferred_language=random.choice(['en', 'hi', 'es', 'fr']),
                travel_style=random.choice(['adventure', 'luxury', 'budget', 'family', 'solo']),
                email_notifications=random.choice([True, False]),
                sms_notifications=random.choice([True, False])
            )
            users.append(user)
            self.stdout.write(f'Created user: {user.email}')

        # Create sample destinations
        destinations = []
        destination_names = ['Paris', 'Tokyo', 'New York', 'Rome', 'Bali']
        for name in destination_names:
            destination = Destination.objects.create(
                name=name,
                description=f'Beautiful {name} with amazing attractions',
                country=name if name != 'New York' else 'USA',
                image=f'destinations/{name.lower()}.jpg'
            )
            destinations.append(destination)
            self.stdout.write(f'Created destination: {name}')

        # Create sample categories
        categories = []
        category_names = ['Adventure', 'Cultural', 'Beach', 'City', 'Nature']
        for name in category_names:
            category = Category.objects.create(
                name=name,
                description=f'{name} tours and experiences'
            )
            categories.append(category)
            self.stdout.write(f'Created category: {name}')

        # Create sample tours
        tours = []
        for i in range(1, 11):
            tour = Tour.objects.create(
                name=f'Sample Tour {i}',
                description=f'This is a sample tour description {i}',
                price=random.randint(100, 1000),
                duration=random.randint(1, 14),
                max_participants=random.randint(5, 30),
                destination=random.choice(destinations),
                category=random.choice(categories),
                start_date=datetime.now() + timedelta(days=random.randint(1, 30)),
                end_date=datetime.now() + timedelta(days=random.randint(31, 60)),
                is_active=True
            )
            tours.append(tour)
            self.stdout.write(f'Created tour: {tour.name}')

        # Create sample wishlist items
        for user in users:
            # Add 2-3 random tours to each user's wishlist
            user_tours = random.sample(tours, random.randint(2, 3))
            for tour in user_tours:
                Wishlist.objects.create(user=user, tour=tour)
                self.stdout.write(f'Added tour {tour.name} to {user.email}\'s wishlist')

        self.stdout.write(self.style.SUCCESS('Successfully populated sample data!')) 