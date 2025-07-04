from django.core.management.base import BaseCommand
from django.core.files import File
from core.models import DestinationCategory, Destination
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Populates the database with sample destinations and categories'

    def handle(self, *args, **options):
        # Create categories
        categories = [
            {'name': 'Beach', 'icon': 'fas fa-umbrella-beach'},
            {'name': 'Mountain', 'icon': 'fas fa-mountain'},
            {'name': 'City', 'icon': 'fas fa-city'},
            {'name': 'Adventure', 'icon': 'fas fa-hiking'},
            {'name': 'Cultural', 'icon': 'fas fa-landmark'},
        ]
        
        for cat_data in categories:
            category, created = DestinationCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={'icon': cat_data['icon']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))
        
        # Create sample destinations
        destinations = [
            {
                'name': 'Bali Island',
                'city': 'Bali',
                'country': 'Indonesia',
                'description': 'Famous for its volcanic mountains, iconic rice paddies, beaches and coral reefs.',
                'category': 'Beach',
                'image': 'bali.jpg',
                'is_featured': True,
                'min_price': 899
            },
            {
                'name': 'Santorini',
                'city': 'Santorini',
                'country': 'Greece',
                'description': 'Known for white-washed houses with blue domes overlooking the caldera.',
                'category': 'Beach',
                'image': 'santorini.jpg',
                'is_featured': True,
                'min_price': 1299
            },
            {
                'name': 'Swiss Alps',
                'city': 'Zermatt',
                'country': 'Switzerland',
                'description': 'Home to the Matterhorn with world-class skiing and mountaineering.',
                'category': 'Mountain',
                'image': 'swiss-alps.jpg',
                'min_price': 1599
            },
            {
                'name': 'Tokyo City',
                'city': 'Tokyo',
                'country': 'Japan',
                'description': 'A bustling metropolis blending ultramodern and traditional attractions.',
                'category': 'City',
                'image': 'tokyo.jpg',
                'min_price': 1499
            },
            {
                'name': 'Machu Picchu',
                'city': 'Cusco',
                'country': 'Peru',
                'description': 'Ancient Incan city high in the Andes mountains with breathtaking views.',
                'category': 'Adventure',
                'image': 'machu-picchu.jpg',
                'is_featured': True,
                'min_price': 1099
            },
            {
                'name': 'Paris',
                'city': 'Paris',
                'country': 'France',
                'description': 'The City of Light, famous for its art, fashion, gastronomy and culture.',
                'category': 'City',
                'image': 'paris.jpg',
                'min_price': 999
            },
            {
                'name': 'Grand Canyon',
                'city': 'Arizona',
                'country': 'USA',
                'description': 'Massive canyon carved by the Colorado River with stunning layered bands of red rock.',
                'category': 'Adventure',
                'image': 'grand-canyon.jpg',
                'min_price': 799
            },
            {
                'name': 'Rome',
                'city': 'Rome',
                'country': 'Italy',
                'description': 'The Eternal City with nearly 3,000 years of globally influential art and architecture.',
                'category': 'Cultural',
                'image': 'rome.jpg',
                'min_price': 899
            }
        ]
        
        # Get sample images from a directory or use placeholders
        image_dir = os.path.join(settings.BASE_DIR, 'sample_images')
        
        for dest_data in destinations:
            category = DestinationCategory.objects.get(name=dest_data['category'])
            
            # Create the destination
            destination, created = Destination.objects.get_or_create(
                name=dest_data['name'],
                city=dest_data['city'],
                country=dest_data['country'],
                defaults={
                    'description': dest_data['description'],
                    'category': category,
                    'is_featured': dest_data.get('is_featured', False),
                    'min_price': dest_data['min_price']
                }
            )
            
            # Add image if it doesn't exist
            if created and not destination.image:
                image_path = os.path.join(image_dir, dest_data['image'])
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as f:
                        destination.image.save(dest_data['image'], File(f))
                        destination.save()
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created destination: {destination.name}')) 