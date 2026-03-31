"""
Test suite for the travel app.

Tests cover models, views, forms, and edge cases.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import date

from .models import Destination, TourPackage, Booking, Review
from .forms import BookingForm, ReviewForm


# ============================================================================
# MODEL TESTS
# ============================================================================


class DestinationModelTest(TestCase):
    """Test cases for Destination model."""

    def setUp(self):
        """Set up test data."""
        self.destination = Destination.objects.create(
            name="Paris",
            description="City of lights",
            location="France",
            image="destinations/paris.jpg"
        )

    def test_destination_creation(self):
        """Test destination is created correctly."""
        self.assertEqual(self.destination.name, "Paris")
        self.assertEqual(self.destination.location, "France")

    def test_destination_str(self):
        """Test destination string representation."""
        self.assertEqual(str(self.destination), "Paris")


class TourPackageModelTest(TestCase):
    """Test cases for TourPackage model."""

    def setUp(self):
        """Set up test data."""
        self.destination = Destination.objects.create(
            name="Tokyo",
            description="Capital of Japan",
            location="Japan",
            image="destinations/tokyo.jpg"
        )
        self.package = TourPackage.objects.create(
            title="Tokyo Adventure",
            destination=self.destination,
            description="Explore Tokyo",
            price=Decimal("1500.00"),
            duration=7,
            max_participants=20,
            difficulty="moderate",
            included_services="Hotel, Meals, Guide",
            image="packages/tokyo.jpg"
        )

    def test_package_creation(self):
        """Test package is created correctly."""
        self.assertEqual(self.package.title, "Tokyo Adventure")
        self.assertEqual(self.package.price, Decimal("1500.00"))
        self.assertEqual(self.package.duration, 7)

    def test_package_str(self):
        """Test package string representation."""
        self.assertEqual(str(self.package), "Tokyo Adventure - Tokyo")

    def test_package_difficulty_choices(self):
        """Test package difficulty choices."""
        self.assertIn(self.package.difficulty, ['easy', 'moderate', 'challenging'])

    def test_package_ordering(self):
        """Test packages are ordered by created_at descending."""
        package2 = TourPackage.objects.create(
            title="Sydney Tour",
            destination=self.destination,
            description="Explore Sydney",
            price=Decimal("1200.00"),
            duration=5,
            difficulty="easy",
            included_services="Hotel, Guide",
            image="packages/sydney.jpg"
        )
        packages = list(TourPackage.objects.all())
        self.assertEqual(packages[0], package2)


class BookingModelTest(TestCase):
    """Test cases for Booking model."""

    def setUp(self):
        """Set up test data."""
        self.destination = Destination.objects.create(
            name="Barcelona",
            description="Gaudí city",
            location="Spain",
            image="destinations/barcelona.jpg"
        )
        self.package = TourPackage.objects.create(
            title="Barcelona Tour",
            destination=self.destination,
            description="Explore Barcelona",
            price=Decimal("999.00"),
            duration=4,
            difficulty="easy",
            included_services="Hotel, Guide",
            image="packages/barcelona.jpg"
        )
        self.booking = Booking.objects.create(
            user_name="John Doe",
            email="john@example.com",
            phone="1234567890",
            package=self.package,
            number_of_participants=2,
            booking_date=date.today()
        )

    def test_booking_creation(self):
        """Test booking is created correctly."""
        self.assertEqual(self.booking.user_name, "John Doe")
        self.assertEqual(self.booking.number_of_participants, 2)

    def test_booking_status_default(self):
        """Test booking status defaults to pending."""
        self.assertEqual(self.booking.status, "pending")


class ReviewModelTest(TestCase):
    """Test cases for Review model."""

    def setUp(self):
        """Set up test data."""
        self.destination = Destination.objects.create(
            name="Rome",
            description="Eternal city",
            location="Italy",
            image="destinations/rome.jpg"
        )
        self.package = TourPackage.objects.create(
            title="Rome Tour",
            destination=self.destination,
            description="Explore Rome",
            price=Decimal("850.00"),
            duration=3,
            difficulty="easy",
            included_services="Hotel, Guide",
            image="packages/rome.jpg"
        )
        self.review = Review.objects.create(
            package=self.package,
            rating=5,
            comment="Amazing experience!"
        )

    def test_review_creation(self):
        """Test review is created correctly."""
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.comment, "Amazing experience!")


# ============================================================================
# VIEW TESTS
# ============================================================================


class HomeViewTest(TestCase):
    """Test cases for home view."""

    def setUp(self):
        """Set up test client."""
        self.client = Client()
        self.destination = Destination.objects.create(
            name="New York",
            description="The big apple",
            location="USA",
            image="destinations/ny.jpg"
        )
        self.package = TourPackage.objects.create(
            title="New York Tour",
            destination=self.destination,
            description="Explore NYC",
            price=Decimal("1100.00"),
            duration=5,
            difficulty="easy",
            included_services="Hotel, Guide",
            image="packages/ny.jpg"
        )

    def test_home_view_status_code(self):
        """Test home view returns 200."""
        response = self.client.get(reverse('travel:home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_uses_correct_template(self):
        """Test home view uses correct template."""
        response = self.client.get(reverse('travel:home'))
        self.assertTemplateUsed(response, 'travel/home.html')

    def test_home_view_context(self):
        """Test home view passes correct context."""
        response = self.client.get(reverse('travel:home'))
        self.assertIn('destinations', response.context)
        self.assertIn('featured_packages', response.context)


class DestinationListViewTest(TestCase):
    """Test cases for destination list view."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        for i in range(15):
            Destination.objects.create(
                name=f"Destination {i}",
                description=f"Description {i}",
                location=f"Location {i}",
                image=f"destinations/dest{i}.jpg"
            )

    def test_destination_list_view_status_code(self):
        """Test destination list view returns 200."""
        response = self.client.get(reverse('travel:destination_list'))
        self.assertEqual(response.status_code, 200)

    def test_destination_list_pagination(self):
        """Test destination list pagination."""
        response = self.client.get(reverse('travel:destination_list'))
        self.assertTrue(response.context['destinations'].has_next())

    def test_destination_list_page_two(self):
        """Test destination list page 2."""
        response = self.client.get(reverse('travel:destination_list') + '?page=2')
        self.assertEqual(response.status_code, 200)


class PackageListViewTest(TestCase):
    """Test cases for package list view."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.destination = Destination.objects.create(
            name="Test Destination",
            description="Test",
            location="Test Location",
            image="destinations/test.jpg"
        )
        for i in range(12):
            TourPackage.objects.create(
                title=f"Package {i}",
                destination=self.destination,
                description=f"Description {i}",
                price=Decimal(f"{500 + i * 100}.00"),
                duration=5 + i,
                difficulty='easy' if i % 3 == 0 else 'moderate',
                included_services="Hotel, Guide",
                image=f"packages/pkg{i}.jpg"
            )

    def test_package_list_view_status_code(self):
        """Test package list view returns 200."""
        response = self.client.get(reverse('travel:package_list'))
        self.assertEqual(response.status_code, 200)

    def test_package_list_with_difficulty_filter(self):
        """Test package list with difficulty filter."""
        response = self.client.get(
            reverse('travel:package_list'),
            {'difficulty': 'easy'}
        )
        self.assertEqual(response.status_code, 200)
        for package in response.context['packages']:
            self.assertEqual(package.difficulty, 'easy')

    def test_package_list_with_price_filter(self):
        """Test package list with price range filter."""
        response = self.client.get(
            reverse('travel:package_list'),
            {'min_price': '500', 'max_price': '1000'}
        )
        self.assertEqual(response.status_code, 200)

    def test_package_list_invalid_price_filter(self):
        """Test package list with invalid price filter."""
        response = self.client.get(
            reverse('travel:package_list'),
            {'min_price': 'invalid', 'max_price': '1000'}
        )
        self.assertEqual(response.status_code, 200)


class PackageDetailViewTest(TestCase):
    """Test cases for package detail view."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.destination = Destination.objects.create(
            name="Test Destination",
            description="Test",
            location="Test Location",
            image="destinations/test.jpg"
        )
        self.package = TourPackage.objects.create(
            title="Test Package",
            destination=self.destination,
            description="Test description",
            price=Decimal("999.00"),
            duration=5,
            difficulty="moderate",
            included_services="Hotel, Guide",
            image="packages/test.jpg"
        )

    def test_package_detail_view_status_code(self):
        """Test package detail view returns 200."""
        response = self.client.get(
            reverse('travel:package_detail', args=[self.package.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_package_detail_view_uses_correct_template(self):
        """Test package detail view uses correct template."""
        response = self.client.get(
            reverse('travel:package_detail', args=[self.package.pk])
        )
        self.assertTemplateUsed(response, 'travel/package_detail.html')

    def test_package_detail_context(self):
        """Test package detail view passes correct context."""
        response = self.client.get(
            reverse('travel:package_detail', args=[self.package.pk])
        )
        self.assertEqual(response.context['package'], self.package)
        self.assertIn('booking_form', response.context)
        self.assertIn('review_form', response.context)

    def test_package_detail_nonexistent(self):
        """Test package detail view with nonexistent package."""
        response = self.client.get(
            reverse('travel:package_detail', args=[9999])
        )
        self.assertEqual(response.status_code, 404)


class SearchPackagesViewTest(TestCase):
    """Test cases for search packages view."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.destination = Destination.objects.create(
            name="Paris",
            description="City of lights",
            location="France",
            image="destinations/paris.jpg"
        )
        TourPackage.objects.create(
            title="Paris City Tour",
            destination=self.destination,
            description="Explore the streets of Paris",
            price=Decimal("899.00"),
            duration=4,
            difficulty="easy",
            included_services="Hotel, Guide",
            image="packages/paris.jpg"
        )

    def test_search_view_no_query(self):
        """Test search view without query."""
        response = self.client.get(reverse('travel:search_packages'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['packages']), 0)

    def test_search_view_with_title_query(self):
        """Test search view with title query."""
        response = self.client.get(
            reverse('travel:search_packages'),
            {'q': 'Paris'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.context['packages']), 0)

    def test_search_view_with_description_query(self):
        """Test search view with description query."""
        response = self.client.get(
            reverse('travel:search_packages'),
            {'q': 'streets'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.context['packages']), 0)


class LoginViewTest(TestCase):
    """Test cases for login view."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_login_view_get_status_code(self):
        """Test login view GET returns 200."""
        response = self.client.get(reverse('travel:login'))
        self.assertEqual(response.status_code, 200)

    def test_login_view_uses_correct_template(self):
        """Test login view uses correct template."""
        response = self.client.get(reverse('travel:login'))
        self.assertTemplateUsed(response, 'travel/login.html')

    def test_login_successful(self):
        """Test successful login."""
        response = self.client.post(
            reverse('travel:login'),
            {'username': 'testuser', 'password': 'testpass123'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_with_wrong_password(self):
        """Test login with wrong password."""
        response = self.client.post(
            reverse('travel:login'),
            {'username': 'testuser', 'password': 'wrongpass'}
        )
        self.assertEqual(response.status_code, 200)


class RegisterViewTest(TestCase):
    """Test cases for register view."""

    def setUp(self):
        """Set up test client."""
        self.client = Client()

    def test_register_view_get_status_code(self):
        """Test register view GET returns 200."""
        response = self.client.get(reverse('travel:register'))
        self.assertEqual(response.status_code, 200)

    def test_register_view_uses_correct_template(self):
        """Test register view uses correct template."""
        response = self.client.get(reverse('travel:register'))
        self.assertTemplateUsed(response, 'travel/register.html')

    def test_register_successful(self):
        """Test successful registration."""
        response = self.client.post(
            reverse('travel:register'),
            {
                'username': 'newuser',
                'password1': 'SecurePass123!',
                'password2': 'SecurePass123!'
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='newuser').exists())


# ============================================================================
# FORM TESTS
# ============================================================================


class BookingFormTest(TestCase):
    """Test cases for BookingForm."""

    def test_booking_form_valid(self):
        """Test valid booking form."""
        form_data = {
            'user_name': 'John Doe',
            'email': 'john@example.com',
            'phone': '1234567890',
            'number_of_participants': 2,
            'booking_date': date.today()
        }
        form = BookingForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_booking_form_missing_required_fields(self):
        """Test booking form with missing required fields."""
        form_data = {}
        form = BookingForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_booking_form_invalid_email(self):
        """Test booking form with invalid email."""
        form_data = {
            'user_name': 'John Doe',
            'email': 'invalid-email',
            'number_of_participants': 2,
            'booking_date': date.today()
        }
        form = BookingForm(data=form_data)
        self.assertFalse(form.is_valid())


class ReviewFormTest(TestCase):
    """Test cases for ReviewForm."""

    def test_review_form_valid(self):
        """Test valid review form."""
        form_data = {
            'rating': 5,
            'comment': 'Great experience!'
        }
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_review_form_invalid_rating(self):
        """Test review form with invalid rating."""
        form_data = {
            'rating': 10,
            'comment': 'Great experience!'
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
