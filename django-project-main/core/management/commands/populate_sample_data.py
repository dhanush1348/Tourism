from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.files import File
from core.models import Destination, Category, Tour, TourImage, Review
from accounts.models import User
import os
from datetime import timedelta

class Command(BaseCommand):
    help = 'Populates the database with sample data'

    def handle(self, *args, **kwargs):
        # Create sample destinations
        destinations = [
            {
                'name': 'Paris',
                'description': 'The city of love and lights',
                'country': 'France',
                'latitude': 48.8566,
                'longitude': 2.3522,
            },
            {
                'name': 'Tokyo',
                'description': 'A vibrant mix of traditional and modern',
                'country': 'Japan',
                'latitude': 35.6762,
                'longitude': 139.6503,
            },
            {
                'name': 'New York',
                'description': 'The city that never sleeps',
                'country': 'USA',
                'latitude': 40.7128,
                'longitude': -74.0060,
            },
        ]

        for dest_data in destinations:
            Destination.objects.get_or_create(
                name=dest_data['name'],
                defaults=dest_data
            )

        # Create sample categories
        categories = [
            {'name': 'Adventure', 'description': 'Thrilling outdoor activities'},
            {'name': 'Cultural', 'description': 'Explore local traditions and heritage'},
            {'name': 'Relaxation', 'description': 'Peaceful and rejuvenating experiences'},
        ]

        for cat_data in categories:
            Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )

        # Create sample tours
        tours = [
            {
                'name': 'Paris City Tour',
                'description': 'Explore the iconic landmarks of Paris',
                'price': 299.99,
                'duration': 3,
                'max_group_size': 20,
                'destination': Destination.objects.get(name='Paris'),
                'category': Category.objects.get(name='Cultural'),
                'start_date': timezone.now() + timedelta(days=30),
                'end_date': timezone.now() + timedelta(days=33),
            },
            {
                'name': 'Tokyo Adventure',
                'description': 'Experience the best of Tokyo',
                'price': 499.99,
                'duration': 5,
                'max_group_size': 15,
                'destination': Destination.objects.get(name='Tokyo'),
                'category': Category.objects.get(name='Adventure'),
                'start_date': timezone.now() + timedelta(days=45),
                'end_date': timezone.now() + timedelta(days=50),
            },
            {
                'name': 'New York Getaway',
                'description': 'Relax in the heart of New York',
                'price': 399.99,
                'duration': 4,
                'max_group_size': 25,
                'destination': Destination.objects.get(name='New York'),
                'category': Category.objects.get(name='Relaxation'),
                'start_date': timezone.now() + timedelta(days=60),
                'end_date': timezone.now() + timedelta(days=64),
            },
        ]

        for tour_data in tours:
            tour, created = Tour.objects.get_or_create(
                name=tour_data['name'],
                defaults=tour_data
            )

            # Create sample reviews for each tour
            for i in range(3):
                Review.objects.get_or_create(
                    tour=tour,
                    user=User.objects.first(),  # Use the first user as reviewer
                    rating=i + 3,  # Ratings from 3 to 5
                    comment=f'Sample review {i + 1} for {tour.name}',
                )

        self.stdout.write(self.style.SUCCESS('Successfully populated sample data')) 