from django.core.management.base import BaseCommand
from travel.models import Destination, TourPackage
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

class Command(BaseCommand):
    help = 'Creates sample destinations and tour packages'

    def handle(self, *args, **kwargs):
        # Create destinations
        destinations = [
            {
                'name': 'Paris, France',
                'description': 'The City of Light, famous for its art, culture, and romance.',
                'location': 'Europe',
            },
            {
                'name': 'Bali, Indonesia',
                'description': 'Tropical paradise with beautiful beaches and rich culture.',
                'location': 'Asia',
            },
            {
                'name': 'New York City, USA',
                'description': 'The Big Apple, a vibrant metropolis and cultural hub.',
                'location': 'North America',
            },
        ]

        for dest_data in destinations:
            destination = Destination.objects.create(**dest_data)
            self.stdout.write(f'Created destination: {destination.name}')

        # Create tour packages
        packages = [
            {
                'title': 'Romantic Paris Getaway',
                'description': 'Experience the romance of Paris with this luxury package including Eiffel Tower dinner.',
                'price': 2499.99,
                'duration': 7,
                'difficulty': 'easy',
                'included_services': 'Hotel, Meals, Tours, Airport Transfer',
                'destination': 'Paris, France',
            },
            {
                'title': 'Bali Beach Paradise',
                'description': 'Relax on pristine beaches and enjoy luxury spa treatments in tropical Bali.',
                'price': 1899.99,
                'duration': 10,
                'difficulty': 'easy',
                'included_services': 'Resort Stay, Breakfast, Beach Activities, Spa',
                'destination': 'Bali, Indonesia',
            },
            {
                'title': 'NYC Adventure',
                'description': 'Explore the bustling streets of New York with this exciting city adventure package.',
                'price': 2199.99,
                'duration': 5,
                'difficulty': 'moderate',
                'included_services': 'Hotel, City Pass, Broadway Show, Tours',
                'destination': 'New York City, USA',
            },
            {
                'title': 'Bali Adventure Trek',
                'description': 'Challenging trek through Bali\'s volcanic landscapes and lush jungles.',
                'price': 1499.99,
                'duration': 7,
                'difficulty': 'challenging',
                'included_services': 'Accommodation, Guide, Equipment, Meals',
                'destination': 'Bali, Indonesia',
            },
        ]

        for package_data in packages:
            dest_name = package_data.pop('destination')
            destination = Destination.objects.get(name=dest_name)
            package = TourPackage.objects.create(
                destination=destination,
                **package_data
            )
            self.stdout.write(f'Created package: {package.title}')
