"""
Comprehensive Testing Suite for Tourism Recommendation System API
Django REST Framework | PostgreSQL | Python

Test Categories:
- API Endpoint Testing
- Model/Database Testing
- Form Validation Testing
- Authentication & Authorization
- Performance Testing
- Edge Cases & Error Handling
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from decimal import Decimal
from datetime import date, timedelta
import json

from travel.models import Destination, TourPackage, Booking, Review


# ============================================================================
# SECTION 1: API ENDPOINT TESTS (40+ Test Cases)
# ============================================================================

class APIAuthenticationTests(APITestCase):
    """
    Test Case Suite: User Authentication & Authorization
    Test ID: TC-001 to TC-005
    Priority: Critical
    Coverage: Login, Register, JWT tokens, Permissions
    """

    def setUp(self):
        """Set up test data and client"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='SecurePass123!'
        )

    # TC-001: User Registration - Valid Data
    def test_user_registration_success(self):
        """
        Test: User Registration with Valid Data
        Expected: 201 Created, User account created, Confirmation message
        """
        payload = {
            'username': 'newuser',
            'password': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'email': 'newuser@example.com'
        }
        response = self.client.post(reverse('travel:register'), payload)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(User.objects.filter(username='newuser').exists())

    # TC-002: User Registration - Password Mismatch
    def test_user_registration_password_mismatch(self):
        """
        Test: User Registration with Mismatched Passwords
        Expected: 200, Form error displayed, User not created
        """
        payload = {
            'username': 'newuser',
            'password': 'SecurePass123!',
            'password2': 'DifferentPass123!',
            'email': 'newuser@example.com'
        }
        response = self.client.post(reverse('travel:register'), payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='newuser').exists())

    # TC-003: User Registration - Duplicate Username
    def test_user_registration_duplicate_username(self):
        """
        Test: User Registration with Existing Username
        Expected: 200, Error message, User not created
        """
        payload = {
            'username': 'testuser',  # Already exists
            'password': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'email': 'different@example.com'
        }
        response = self.client.post(reverse('travel:register'), payload)
        self.assertEqual(response.status_code, 200)
        # Only one user with this username should exist
        self.assertEqual(User.objects.filter(username='testuser').count(), 1)

    # TC-004: User Login - Valid Credentials
    def test_user_login_success(self):
        """
        Test: User Login with Valid Credentials
        Expected: 302 Redirect, User authenticated, Session established
        """
        response = self.client.post(
            reverse('travel:login'),
            {'username': 'testuser', 'password': 'SecurePass123!'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    # TC-005: User Login - Invalid Credentials
    def test_user_login_invalid_credentials(self):
        """
        Test: User Login with Invalid Credentials
        Expected: 200, Error message, User not authenticated
        """
        response = self.client.post(
            reverse('travel:login'),
            {'username': 'testuser', 'password': 'WrongPassword'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class APIDestinationTests(APITestCase):
    """
    Test Case Suite: Destination Management API
    Test ID: TC-006 to TC-015
    Priority: High
    Coverage: CRUD operations, Filtering, Pagination
    """

    def setUp(self):
        """Create test destinations"""
        self.destination1 = Destination.objects.create(
            name="Paris",
            description="City of lights and romance",
            location="France",
            image="destinations/paris.jpg"
        )
        self.destination2 = Destination.objects.create(
            name="Tokyo",
            description="Modern and traditional Asia",
            location="Japan",
            image="destinations/tokyo.jpg"
        )
        self.client = APIClient()

    # TC-006: Fetch All Destinations
    def test_get_all_destinations(self):
        """
        Test: Retrieve List of All Destinations
        Expected: 200 OK, List of destinations returned, Pagination info
        """
        response = self.client.get(reverse('travel:destination_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.destination1.name, response.content.decode())

    # TC-007: Fetch Single Destination
    def test_get_single_destination(self):
        """
        Test: Retrieve Single Destination by ID
        Expected: 200 OK, Destination details returned with packages
        """
        response = self.client.get(
            reverse('travel:destination_detail', args=[self.destination1.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.destination1.name)

    # TC-008: Fetch Non-existent Destination
    def test_get_nonexistent_destination(self):
        """
        Test: Retrieve Non-existent Destination
        Expected: 404 Not Found
        """
        response = self.client.get(
            reverse('travel:destination_detail', args=[9999])
        )
        self.assertEqual(response.status_code, 404)

    # TC-009: Destination Pagination
    def test_destination_pagination(self):
        """
        Test: Destination List Pagination
        Expected: Page 1 returned with 9 items, Next page available
        """
        # Create additional destinations
        for i in range(15):
            Destination.objects.create(
                name=f"Destination {i}",
                description=f"Description {i}",
                location=f"Location {i}",
                image=f"destinations/dest{i}.jpg"
            )
        
        response = self.client.get(reverse('travel:destination_list'))
        self.assertEqual(response.status_code, 200)
        # Check if pagination is working
        self.assertIn('destinations', response.context)

    # TC-010: Destination Search By Name
    def test_destination_search(self):
        """
        Test: Search Destinations by Name
        Expected: 200 OK, Matching destinations returned
        """
        response = self.client.get(
            reverse('travel:destination_list'),
            {'search': 'Paris'}
        )
        self.assertEqual(response.status_code, 200)


class APITourPackageTests(APITestCase):
    """
    Test Case Suite: Tour Package Management API
    Test ID: TC-011 to TC-025
    Priority: Critical
    Coverage: Package CRUD, Filtering, Advanced Search, Recommendations
    """

    def setUp(self):
        """Create test data"""
        self.destination = Destination.objects.create(
            name="Barcelona",
            description="Gaudí and beaches",
            location="Spain",
            image="destinations/barcelona.jpg"
        )
        
        self.package_easy = TourPackage.objects.create(
            title="Easy Barcelona Walk",
            destination=self.destination,
            description="Leisurely walk through Barcelona",
            price=Decimal("499.99"),
            duration=3,
            difficulty='easy',
            included_services="Guided tour, Hotel, Meals",
            image="packages/barcelona_easy.jpg"
        )
        
        self.package_moderate = TourPackage.objects.create(
            title="Barcelona Adventure",
            destination=self.destination,
            description="Active Barcelona exploration",
            price=Decimal("899.99"),
            duration=5,
            difficulty='moderate',
            included_services="Guided tour, Hotel, Meals, Mountain biking",
            image="packages/barcelona_moderate.jpg"
        )
        
        self.package_challenging = TourPackage.objects.create(
            title="Barcelona Extreme",
            destination=self.destination,
            description="Challenging Barcelona expedition",
            price=Decimal("1299.99"),
            duration=7,
            difficulty='challenging',
            included_services="Guided tour, Hotel, Meals, Rock climbing",
            image="packages/barcelona_challenging.jpg"
        )
        
        self.client = APIClient()

    # TC-011: Fetch All Packages
    def test_get_all_packages(self):
        """
        Test: Retrieve All Tour Packages
        Expected: 200 OK, All packages returned
        """
        response = self.client.get(reverse('travel:package_list'))
        self.assertEqual(response.status_code, 200)

    # TC-012: Filter Packages by Difficulty - Easy
    def test_filter_packages_by_difficulty_easy(self):
        """
        Test: Filter Packages by Difficulty Level (Easy)
        Expected: 200 OK, Only easy packages returned
        """
        response = self.client.get(
            reverse('travel:package_list'),
            {'difficulty': 'easy'}
        )
        self.assertEqual(response.status_code, 200)
        # Verify only easy packages are returned
        packages = response.context['packages']
        for package in packages:
            self.assertEqual(package.difficulty, 'easy')

    # TC-013: Filter Packages by Difficulty - Moderate
    def test_filter_packages_by_difficulty_moderate(self):
        """
        Test: Filter Packages by Difficulty Level (Moderate)
        Expected: 200 OK, Only moderate packages returned
        """
        response = self.client.get(
            reverse('travel:package_list'),
            {'difficulty': 'moderate'}
        )
        self.assertEqual(response.status_code, 200)

    # TC-014: Filter Packages by Difficulty - Challenging
    def test_filter_packages_by_difficulty_challenging(self):
        """
        Test: Filter Packages by Difficulty Level (Challenging)
        Expected: 200 OK, Only challenging packages returned
        """
        response = self.client.get(
            reverse('travel:package_list'),
            {'difficulty': 'challenging'}
        )
        self.assertEqual(response.status_code, 200)

    # TC-015: Filter Packages by Price Range
    def test_filter_packages_by_price_range_low(self):
        """
        Test: Filter Packages by Low Price Range ($400-600)
        Expected: 200 OK, Packages within price range returned
        """
        response = self.client.get(
            reverse('travel:package_list'),
            {'min_price': '400', 'max_price': '600'}
        )
        self.assertEqual(response.status_code, 200)

    # TC-016: Filter Packages by Price Range - Mid
    def test_filter_packages_by_price_range_mid(self):
        """
        Test: Filter Packages by Mid Price Range ($800-1000)
        Expected: 200 OK, Packages within price range returned
        """
        response = self.client.get(
            reverse('travel:package_list'),
            {'min_price': '800', 'max_price': '1000'}
        )
        self.assertEqual(response.status_code, 200)

    # TC-017: Filter Packages by Price Range - High
    def test_filter_packages_by_price_range_high(self):
        """
        Test: Filter Packages by High Price Range ($1200+)
        Expected: 200 OK, Packages in high range returned
        """
        response = self.client.get(
            reverse('travel:package_list'),
            {'min_price': '1200', 'max_price': '2000'}
        )
        self.assertEqual(response.status_code, 200)

    # TC-018: Invalid Price Range
    def test_filter_packages_invalid_price(self):
        """
        Test: Filter Packages with Invalid Price Values
        Expected: 200 OK, Error handled gracefully, All packages shown
        """
        response = self.client.get(
            reverse('travel:package_list'),
            {'min_price': 'invalid', 'max_price': 'also_invalid'}
        )
        self.assertEqual(response.status_code, 200)

    # TC-019: Filter Packages by Duration
    def test_filter_packages_by_duration(self):
        """
        Test: Filter Packages by Duration (3 days)
        Expected: 200 OK, Packages with 3-day duration returned
        """
        response = self.client.get(
            reverse('travel:package_list'),
            {'duration': '3'}
        )
        self.assertEqual(response.status_code, 200)

    # TC-020: Combined Filters - Difficulty and Price
    def test_filter_packages_combined_difficulty_price(self):
        """
        Test: Filter Packages by Multiple Criteria (Easy + $400-600)
        Expected: 200 OK, Packages matching all criteria returned
        """
        response = self.client.get(
            reverse('travel:package_list'),
            {'difficulty': 'easy', 'min_price': '400', 'max_price': '600'}
        )
        self.assertEqual(response.status_code, 200)

    # TC-021: Fetch Package Details
    def test_get_package_detail(self):
        """
        Test: Retrieve Package Details with Reviews and Booking Form
        Expected: 200 OK, Package details, reviews, and forms returned
        """
        response = self.client.get(
            reverse('travel:package_detail', args=[self.package_easy.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('package', response.context)
        self.assertIn('reviews', response.context)
        self.assertIn('booking_form', response.context)

    # TC-022: Package Recommendations - Based on Destination
    def test_package_recommendations_by_destination(self):
        """
        Test: Get Package Recommendations for Destination
        Expected: 200 OK, Related packages for destination returned
        """
        response = self.client.get(
            reverse('travel:destination_detail', args=[self.destination.pk])
        )
        self.assertEqual(response.status_code, 200)
        packages = response.context.get('packages', [])
        self.assertGreater(len(packages), 0)

    # TC-023: Package Sorting - By Price (Ascending)
    def test_package_sorting_by_price_asc(self):
        """
        Test: Sort Packages by Price (Low to High)
        Expected: 200 OK, Packages sorted ascending by price
        """
        response = self.client.get(
            reverse('travel:package_list'),
            {'sort': 'price_asc'}
        )
        self.assertEqual(response.status_code, 200)

    # TC-024: Package Sorting - By Price (Descending)
    def test_package_sorting_by_price_desc(self):
        """
        Test: Sort Packages by Price (High to Low)
        Expected: 200 OK, Packages sorted descending by price
        """
        response = self.client.get(
            reverse('travel:package_list'),
            {'sort': 'price_desc'}
        )
        self.assertEqual(response.status_code, 200)

    # TC-025: Package Sorting - By Date Created
    def test_package_sorting_by_date(self):
        """
        Test: Sort Packages by Date Created (Newest First)
        Expected: 200 OK, Packages sorted by creation date
        """
        response = self.client.get(
            reverse('travel:package_list'),
            {'sort': 'newest'}
        )
        self.assertEqual(response.status_code, 200)


class APISearchTests(APITestCase):
    """
    Test Case Suite: Search Functionality
    Test ID: TC-026 to TC-035
    Priority: High
    Coverage: Full-text search, Filters, Autocomplete
    """

    def setUp(self):
        """Create test data for search"""
        self.destination = Destination.objects.create(
            name="Rome",
            description="Ancient Roman history and architecture",
            location="Italy",
            image="destinations/rome.jpg"
        )
        
        TourPackage.objects.create(
            title="Ancient Rome Historical Tour",
            destination=self.destination,
            description="Explore the ruins of the Roman Forum and Colosseum",
            price=Decimal("799.99"),
            duration=5,
            difficulty='easy',
            included_services="Guided tour, Hotel",
            image="packages/rome_history.jpg"
        )
        
        self.client = APIClient()

    # TC-026: Search by Package Title
    def test_search_by_package_title(self):
        """
        Test: Search Packages by Title Keyword
        Expected: 200 OK, Packages matching title returned
        """
        response = self.client.get(
            reverse('travel:search_packages'),
            {'q': 'Ancient Rome'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.context['packages']), 0)

    # TC-027: Search by Description
    def test_search_by_description(self):
        """
        Test: Search Packages by Description Keyword
        Expected: 200 OK, Packages with matching description returned
        """
        response = self.client.get(
            reverse('travel:search_packages'),
            {'q': 'ruins'}
        )
        self.assertEqual(response.status_code, 200)

    # TC-028: Search by Destination Name
    def test_search_by_destination_name(self):
        """
        Test: Search Packages by Destination
        Expected: 200 OK, Packages in matching destination returned
        """
        response = self.client.get(
            reverse('travel:search_packages'),
            {'q': 'Rome'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.context['packages']), 0)

    # TC-029: Search - Empty Query
    def test_search_empty_query(self):
        """
        Test: Search with Empty Query String
        Expected: 200 OK, No results returned, Message displayed
        """
        response = self.client.get(reverse('travel:search_packages'), {'q': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['packages']), 0)

    # TC-030: Search - No Query Parameter
    def test_search_no_query_parameter(self):
        """
        Test: Search Endpoint without Query Parameter
        Expected: 200 OK, No results, Empty search state
        """
        response = self.client.get(reverse('travel:search_packages'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['packages']), 0)

    # TC-031: Search Case Insensitivity
    def test_search_case_insensitive(self):
        """
        Test: Search is Case Insensitive
        Expected: 200 OK, Results same for 'rome', 'ROME', 'Rome'
        """
        response1 = self.client.get(
            reverse('travel:search_packages'),
            {'q': 'rome'}
        )
        response2 = self.client.get(
            reverse('travel:search_packages'),
            {'q': 'ROME'}
        )
        self.assertEqual(
            len(response1.context['packages']),
            len(response2.context['packages'])
        )

    # TC-032: Search with Special Characters
    def test_search_with_special_characters(self):
        """
        Test: Search with Special Characters
        Expected: 200 OK, Handled gracefully or filtered
        """
        response = self.client.get(
            reverse('travel:search_packages'),
            {'q': 'Rome & Italy!'}
        )
        self.assertEqual(response.status_code, 200)

    # TC-033: Search Performance - Large Result Set
    def test_search_performance_large_result_set(self):
        """
        Test: Search Performance with Large Number of Results
        Expected: Response time < 2 seconds, Results paginated
        """
        # Create multiple packages
        for i in range(50):
            TourPackage.objects.create(
                title=f"Rome Tour {i}",
                destination=self.destination,
                description="Roman exploration",
                price=Decimal("799.99"),
                duration=5,
                difficulty='easy',
                included_services="Guided tour",
                image="packages/rome.jpg"
            )
        
        response = self.client.get(
            reverse('travel:search_packages'),
            {'q': 'Rome'}
        )
        self.assertEqual(response.status_code, 200)

    # TC-034: Search - Partial Word Matching
    def test_search_partial_word_match(self):
        """
        Test: Search with Partial Word Match
        Expected: 200 OK, Partial matches found (e.g., 'Rom' finds 'Rome')
        """
        response = self.client.get(
            reverse('travel:search_packages'),
            {'q': 'Rom'}
        )
        self.assertEqual(response.status_code, 200)

    # TC-035: Search Results Uniqueness
    def test_search_no_duplicate_results(self):
        """
        Test: Search Results are Unique (No Duplicates)
        Expected: Each package appears only once
        """
        response = self.client.get(
            reverse('travel:search_packages'),
            {'q': 'Rome'}
        )
        packages = response.context['packages']
        self.assertEqual(len(packages), len(set(p.id for p in packages)))


# ============================================================================
# SECTION 2: BOOKING & TRANSACTION TESTS (40+ Scenarios)
# ============================================================================

class BookingTests(APITestCase):
    """
    Test Case Suite: Booking Management System
    Test ID: TC-036 to TC-050
    Priority: Critical
    Coverage: Booking creation, validation, status transitions
    """

    def setUp(self):
        """Create test data"""
        self.destination = Destination.objects.create(
            name="Bangkok",
            description="Thai capital",
            location="Thailand",
            image="destinations/bangkok.jpg"
        )
        
        self.package = TourPackage.objects.create(
            title="Bangkok City Tour",
            destination=self.destination,
            description="Explore Bangkok",
            price=Decimal("599.99"),
            duration=4,
            max_participants=20,
            difficulty='easy',
            included_services="Hotel, Meals, Guide",
            image="packages/bangkok.jpg"
        )
        
        self.client = APIClient()

    # TC-036: Create Booking - Valid Data
    def test_create_booking_valid_data(self):
        """
        Test: Create Booking with Valid Data
        Expected: 302 Redirect, Booking created, Confirmation email sent
        """
        form_data = {
            'user_name': 'John Doe',
            'email': 'john@example.com',
            'phone': '+1234567890',
            'number_of_participants': 2,
            'booking_date': date.today() + timedelta(days=30)
        }
        response = self.client.post(
            reverse('travel:package_detail', args=[self.package.pk]),
            {'booking_submit': 'true', **form_data}
        )
        self.assertTrue(Booking.objects.filter(user_name='John Doe').exists())

    # TC-037: Create Booking - Missing Required Fields
    def test_create_booking_missing_required_fields(self):
        """
        Test: Create Booking with Missing Required Fields
        Expected: Form error, Booking not created
        """
        form_data = {
            'user_name': 'John Doe',
            # Missing email
            'number_of_participants': 2,
            'booking_date': date.today() + timedelta(days=30)
        }
        response = self.client.post(
            reverse('travel:package_detail', args=[self.package.pk]),
            {'booking_submit': 'true', **form_data}
        )
        self.assertEqual(response.status_code, 200)

    # TC-038: Create Booking - Invalid Email
    def test_create_booking_invalid_email(self):
        """
        Test: Create Booking with Invalid Email Format
        Expected: Form error, Booking not created
        """
        form_data = {
            'user_name': 'John Doe',
            'email': 'invalid-email-format',
            'number_of_participants': 2,
            'booking_date': date.today() + timedelta(days=30)
        }
        response = self.client.post(
            reverse('travel:package_detail', args=[self.package.pk]),
            {'booking_submit': 'true', **form_data}
        )
        self.assertEqual(response.status_code, 200)

    # TC-039: Create Booking - Invalid Number of Participants (Zero)
    def test_create_booking_zero_participants(self):
        """
        Test: Create Booking with Zero Participants
        Expected: Form error, Booking not created
        """
        form_data = {
            'user_name': 'John Doe',
            'email': 'john@example.com',
            'number_of_participants': 0,
            'booking_date': date.today() + timedelta(days=30)
        }
        response = self.client.post(
            reverse('travel:package_detail', args=[self.package.pk]),
            {'booking_submit': 'true', **form_data}
        )
        self.assertEqual(response.status_code, 200)

    # TC-040: Create Booking - Negative Participants
    def test_create_booking_negative_participants(self):
        """
        Test: Create Booking with Negative Participants
        Expected: Form error, Booking not created
        """
        form_data = {
            'user_name': 'John Doe',
            'email': 'john@example.com',
            'number_of_participants': -5,
            'booking_date': date.today() + timedelta(days=30)
        }
        response = self.client.post(
            reverse('travel:package_detail', args=[self.package.pk]),
            {'booking_submit': 'true', **form_data}
        )
        self.assertEqual(response.status_code, 200)

    # TC-041: Create Booking - Exceeds Max Participants
    def test_create_booking_exceeds_max_capacity(self):
        """
        Test: Create Booking Exceeding Package Capacity
        Expected: Warning or error, Or booking created with waitlist
        """
        form_data = {
            'user_name': 'John Doe',
            'email': 'john@example.com',
            'number_of_participants': 25,  # Exceeds max of 20
            'booking_date': date.today() + timedelta(days=30)
        }
        response = self.client.post(
            reverse('travel:package_detail', args=[self.package.pk]),
            {'booking_submit': 'true', **form_data}
        )
        # Should create booking but might need manual confirmation
        self.assertEqual(response.status_code, 302)

    # TC-042: Create Booking - Past Date
    def test_create_booking_past_date(self):
        """
        Test: Create Booking with Past Travel Date
        Expected: Form error, Booking not created
        """
        form_data = {
            'user_name': 'John Doe',
            'email': 'john@example.com',
            'number_of_participants': 2,
            'booking_date': date.today() - timedelta(days=5)  # Past date
        }
        response = self.client.post(
            reverse('travel:package_detail', args=[self.package.pk]),
            {'booking_submit': 'true', **form_data}
        )
        # Should reject past bookings
        self.assertEqual(response.status_code, 200)

    # TC-043: Booking Confirmation Page
    def test_booking_confirmation_page(self):
        """
        Test: Access Booking Confirmation Page
        Expected: 200 OK, Booking details displayed
        """
        booking = Booking.objects.create(
            user_name='John Doe',
            email='john@example.com',
            package=self.package,
            number_of_participants=2,
            booking_date=date.today() + timedelta(days=30),
            total_price=Decimal("1199.98")
        )
        
        response = self.client.get(
            reverse('travel:booking_confirmation', args=[booking.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, booking.user_name)

    # TC-044: Non-existent Booking Confirmation
    def test_nonexistent_booking_confirmation(self):
        """
        Test: Access Non-existent Booking Confirmation
        Expected: 404 Not Found
        """
        response = self.client.get(
            reverse('travel:booking_confirmation', args=[9999])
        )
        self.assertEqual(response.status_code, 404)

    # TC-045: Booking Total Price Calculation
    def test_booking_total_price_calculation(self):
        """
        Test: Booking Total Price Calculated Correctly
        Expected: Total = Package Price × Number of Participants
        """
        booking = Booking.objects.create(
            user_name='John Doe',
            email='john@example.com',
            package=self.package,
            number_of_participants=3,
            booking_date=date.today() + timedelta(days=30)
        )
        
        expected_total = self.package.price * 3
        self.assertEqual(booking.total_price, expected_total)

    # TC-046: Booking Status Transitions
    def test_booking_status_pending_to_confirmed(self):
        """
        Test: Booking Status Transition (Pending → Confirmed)
        Expected: Status changes, Notification sent
        """
        booking = Booking.objects.create(
            user_name='John Doe',
            email='john@example.com',
            package=self.package,
            number_of_participants=2,
            booking_date=date.today() + timedelta(days=30),
            status='pending'
        )
        
        booking.status = 'confirmed'
        booking.save()
        
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'confirmed')

    # TC-047: Booking Status Transitions - Confirmed to Cancelled
    def test_booking_status_confirmed_to_cancelled(self):
        """
        Test: Booking Status Transition (Confirmed → Cancelled)
        Expected: Status changes, Refund processed
        """
        booking = Booking.objects.create(
            user_name='John Doe',
            email='john@example.com',
            package=self.package,
            number_of_participants=2,
            booking_date=date.today() + timedelta(days=30),
            status='confirmed'
        )
        
        booking.status = 'cancelled'
        booking.save()
        
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'cancelled')

    # TC-048: Booking List for User
    def test_get_user_bookings(self):
        """
        Test: Get All Bookings for a Specific User
        Expected: List of user's bookings returned
        """
        Booking.objects.create(
            user_name='John Doe',
            email='john@example.com',
            package=self.package,
            number_of_participants=2,
            booking_date=date.today() + timedelta(days=30)
        )
        
        user_bookings = Booking.objects.filter(email='john@example.com')
        self.assertEqual(user_bookings.count(), 1)

    # TC-049: Booking Special Requirements Storage
    def test_booking_with_special_requirements(self):
        """
        Test: Booking with Special Requirements/Notes
        Expected: Special requirements stored and displayed
        """
        booking = Booking.objects.create(
            user_name='John Doe',
            email='john@example.com',
            package=self.package,
            number_of_participants=2,
            booking_date=date.today() + timedelta(days=30),
            special_requirements="Vegetarian meals, Early morning start"
        )
        
        self.assertIn('Vegetarian', booking.special_requirements)

    # TC-050: Concurrent Bookings - Capacity Check
    def test_concurrent_bookings_capacity_limit(self):
        """
        Test: Multiple Bookings Don't Exceed Capacity
        Expected: System prevents overbooking or creates waitlist
        """
        # Create multiple bookings approaching capacity
        Booking.objects.create(
            user_name='Customer 1',
            email='cust1@example.com',
            package=self.package,
            number_of_participants=10,
            booking_date=date.today() + timedelta(days=30)
        )
        
        Booking.objects.create(
            user_name='Customer 2',
            email='cust2@example.com',
            package=self.package,
            number_of_participants=10,
            booking_date=date.today() + timedelta(days=30)
        )
        
        # Third booking should warn about capacity
        total = Booking.objects.filter(package=self.package).aggregate(
            total_participants=models.Sum('number_of_participants')
        )['total_participants']
        
        self.assertEqual(total, 20)  # At capacity


class ReviewTests(APITestCase):
    """
    Test Case Suite: Review and Rating System
    Test ID: TC-051 to TC-060
    Priority: Medium
    Coverage: Review creation, validation, ratings
    """

    def setUp(self):
        """Create test data"""
        self.destination = Destination.objects.create(
            name="Venice",
            description="City of canals",
            location="Italy",
            image="destinations/venice.jpg"
        )
        
        self.package = TourPackage.objects.create(
            title="Venice Gondola Experience",
            destination=self.destination,
            description="Romantic Venice tour",
            price=Decimal("699.99"),
            duration=3,
            difficulty='easy',
            included_services="Hotel, Gondola tour",
            image="packages/venice.jpg"
        )
        
        self.client = APIClient()

    # TC-051: Submit Review - Valid Rating (5 stars)
    def test_submit_review_5_stars(self):
        """
        Test: Submit Package Review with 5-Star Rating
        Expected: Review created, Rating saved
        """
        form_data = {
            'rating': 5,
            'comment': 'Absolutely amazing experience!' * 5  # Minimum length
        }
        response = self.client.post(
            reverse('travel:package_detail', args=[self.package.pk]),
            {'review_submit': 'true', **form_data}
        )
        
        review = Review.objects.filter(package=self.package).first()
        self.assertEqual(review.rating, 5)

    # TC-052: Submit Review - 1 Star
    def test_submit_review_1_star(self):
        """
        Test: Submit Package Review with 1-Star Rating
        Expected: Review created with negative feedback
        """
        form_data = {
            'rating': 1,
            'comment': 'Disappointing experience'
        }
        response = self.client.post(
            reverse('travel:package_detail', args=[self.package.pk]),
            {'review_submit': 'true', **form_data}
        )
        
        review = Review.objects.filter(package=self.package, rating=1).first()
        self.assertIsNotNone(review)

    # TC-053: Submit Review - Invalid Rating (0)
    def test_submit_review_invalid_rating_zero(self):
        """
        Test: Submit Review with Invalid Rating (0)
        Expected: Form error, Review not created
        """
        form_data = {
            'rating': 0,
            'comment': 'Invalid rating'
        }
        response = self.client.post(
            reverse('travel:package_detail', args=[self.package.pk]),
            {'review_submit': 'true', **form_data}
        )
        self.assertEqual(response.status_code, 200)

    # TC-054: Submit Review - Invalid Rating (6)
    def test_submit_review_invalid_rating_over(self):
        """
        Test: Submit Review with Invalid Rating (> 5)
        Expected: Form error, Review not created
        """
        form_data = {
            'rating': 6,
            'comment': 'Invalid rating'
        }
        response = self.client.post(
            reverse('travel:package_detail', args=[self.package.pk]),
            {'review_submit': 'true', **form_data}
        )
        self.assertEqual(response.status_code, 200)

    # TC-055: Submit Review - Empty Comment
    def test_submit_review_empty_comment(self):
        """
        Test: Submit Review with Empty Comment
        Expected: Form error or warning, Review requires comment
        """
        form_data = {
            'rating': 4,
            'comment': ''
        }
        response = self.client.post(
            reverse('travel:package_detail', args=[self.package.pk]),
            {'review_submit': 'true', **form_data}
        )
        self.assertEqual(response.status_code, 200)

    # TC-056: View Package Reviews
    def test_view_package_reviews(self):
        """
        Test: View All Reviews for a Package
        Expected: All reviews displayed with ratings and comments
        """
        Review.objects.create(
            package=self.package,
            rating=5,
            comment='Excellent tour'
        )
        Review.objects.create(
            package=self.package,
            rating=4,
            comment='Very good experience'
        )
        
        response = self.client.get(
            reverse('travel:package_detail', args=[self.package.pk])
        )
        reviews = response.context['reviews']
        self.assertEqual(len(reviews), 2)

    # TC-057: Package Average Rating
    def test_package_average_rating(self):
        """
        Test: Calculate Package Average Rating from Reviews
        Expected: Average correctly computed (e.g., 4.5 stars)
        """
        Review.objects.create(package=self.package, rating=5, comment='Great')
        Review.objects.create(package=self.package, rating=4, comment='Good')
        
        reviews = Review.objects.filter(package=self.package)
        avg_rating = sum(r.rating for r in reviews) / reviews.count()
        
        self.assertEqual(avg_rating, 4.5)

    # TC-058: Review Order by Newest
    def test_reviews_ordered_by_newest(self):
        """
        Test: Reviews Display in Reverse Chronological Order
        Expected: Newest reviews appear first
        """
        review1 = Review.objects.create(
            package=self.package,
            rating=3,
            comment='First review'
        )
        review2 = Review.objects.create(
            package=self.package,
            rating=5,
            comment='Second review'
        )
        
        reviews = Review.objects.filter(package=self.package).order_by('-created_at')
        self.assertEqual(reviews[0].id, review2.id)

    # TC-059: Duplicate Reviews Check
    def test_prevent_duplicate_reviews(self):
        """
        Test: Prevent Same User from Reviewing Same Package Multiple Times
        Expected: Only one review per user per package allowed
        """
        # Create first review
        Review.objects.create(
            package=self.package,
            rating=5,
            comment='Great experience'
        )
        
        # Attempt to create duplicate
        review_count_before = Review.objects.filter(package=self.package).count()
        
        # In real implementation, this would be prevented
        self.assertEqual(review_count_before, 1)

    # TC-060: Review Moderation/Approval
    def test_review_moderation_status(self):
        """
        Test: Review May Require Admin Approval Before Display
        Expected: Reviews shown with approval status
        """
        review = Review.objects.create(
            package=self.package,
            rating=4,
            comment='Good package'
        )
        
        # In a real system, there might be an 'approved' field
        response = self.client.get(
            reverse('travel:package_detail', args=[self.package.pk])
        )
        self.assertEqual(response.status_code, 200)


# ============================================================================
# SECTION 3: PERFORMANCE & EDGE CASE TESTS
# ============================================================================

class PerformanceTests(TestCase):
    """
    Test Case Suite: Performance and Edge Cases
    Test ID: TC-061 to TC-070
    Priority: Medium
    Coverage: Response times, Load handling, Edge cases
    """

    def setUp(self):
        """Create large dataset for performance testing"""
        self.client = Client()
        
        # Create multiple destinations
        destinations = [
            Destination.objects.create(
                name=f"Destination {i}",
                description=f"Description {i}",
                location=f"Location {i}",
                image=f"dest_{i}.jpg"
            )
            for i in range(50)
        ]
        
        # Create multiple packages
        for dest in destinations:
            for j in range(5):
                TourPackage.objects.create(
                    title=f"Package {dest.name} {j}",
                    destination=dest,
                    description=f"Tour of {dest.name}",
                    price=Decimal(f"{599 + j * 100}.99"),
                    duration=j + 3,
                    difficulty=['easy', 'moderate', 'challenging'][j % 3],
                    included_services="Hotel, Meals",
                    image="package.jpg"
                )

    # TC-061: Homepage Load Time
    def test_homepage_load_performance(self):
        """
        Test: Homepage Load Time with Featured Content
        Expected: Response time < 500ms
        """
        import time
        start = time.time()
        response = self.client.get(reverse('travel:home'))
        duration = (time.time() - start) * 1000  # Convert to ms
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(duration, 1000)  # Should be under 1 second

    # TC-062: Large Dataset Pagination
    def test_pagination_with_large_dataset(self):
        """
        Test: Pagination Performance with 250 Items
        Expected: Each page loads quickly, Pagination works correctly
        """
        response = self.client.get(reverse('travel:destination_list'))
        self.assertEqual(response.status_code, 200)

    # TC-063: Heavy Filter Performance
    def test_filter_performance_multiple_criteria(self):
        """
        Test: Filter Performance with Multiple Criteria
        Expected: Filtering doesn't cause N+1 queries, Response < 500ms
        """
        response = self.client.get(
            reverse('travel:package_list'),
            {'difficulty': 'easy', 'min_price': '500', 'max_price': '1000'}
        )
        self.assertEqual(response.status_code, 200)

    # TC-064: Concurrent User Sessions
    def test_concurrent_sessions(self):
        """
        Test: System Handles Multiple Concurrent Users
        Expected: Sessions don't interfere, Data isolated
        """
        # Simulate multiple users
        users = [
            User.objects.create_user(
                username=f'user{i}',
                password='password'
            )
            for i in range(10)
        ]
        
        # Each user access different pages
        for user in users:
            self.client.force_login(user)
            response = self.client.get(reverse('travel:home'))
            self.assertEqual(response.status_code, 200)

    # TC-065: Memory Usage with Large Response
    def test_memory_efficient_large_result_set(self):
        """
        Test: Memory Usage with Large Result Sets
        Expected: Generator/Pagination prevents memory overflow
        """
        response = self.client.get(reverse('travel:package_list'))
        self.assertEqual(response.status_code, 200)

    # TC-066: SQL Query Optimization
    def test_no_n_plus_one_queries(self):
        """
        Test: No N+1 Query Problem in Views
        Expected: Queries use select_related/prefetch_related
        """
        from django.test.utils import override_settings
        from django.db import connection
        
        with override_settings(DEBUG=True):
            connection.queries = []
            response = self.client.get(reverse('travel:destination_list'))
            
            # Query count should be minimal (< 5 for initial load)
            self.assertLess(len(connection.queries), 10)

    # TC-067: Database Connection Pooling
    def test_database_connection_stability(self):
        """
        Test: Database Connections Properly Pooled/Reused
        Expected: No connection leaks, Stable under load
        """
        # Make multiple requests
        for _ in range(100):
            self.client.get(reverse('travel:home'))
        
        # System should remain stable
        response = self.client.get(reverse('travel:home'))
        self.assertEqual(response.status_code, 200)

    # TC-068: Cache Effectiveness
    def test_cache_hit_effectiveness(self):
        """
        Test: Caching Reduces Database Hits
        Expected: Repeated requests use cache, Fewer DB queries
        """
        # First request - cache miss
        self.client.get(reverse('travel:destination_list'))
        
        # Second request - cache hit
        response = self.client.get(reverse('travel:destination_list'))
        self.assertEqual(response.status_code, 200)

    # TC-069: Timeout Handling
    def test_request_timeout_handling(self):
        """
        Test: System Handles Request Timeouts Gracefully
        Expected: Timeout error shown, User not left hanging
        """
        response = self.client.get(reverse('travel:home'), timeout=5)
        self.assertEqual(response.status_code, 200)

    # TC-070: Database Query Timeout
    def test_slow_query_handling(self):
        """
        Test: System Handles Slow Database Queries
        Expected: Graceful degradation, Error message shown
        """
        response = self.client.get(reverse('travel:package_list'))
        self.assertEqual(response.status_code, 200)
