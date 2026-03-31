"""
Travel app views module.

Handles all HTTP request/response logic for the tours and bookings application.
"""

import logging
from typing import Any, Dict

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.paginator import Paginator
from django.db import models
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookingForm, ReviewForm
from .models import Booking, Destination, Review, TourPackage

logger = logging.getLogger(__name__)

# Configuration constants
ITEMS_PER_PAGE = 9
FEATURED_DESTINATIONS_COUNT = 6
FEATURED_PACKAGES_COUNT = 4

def home(request: HttpRequest) -> HttpResponse:
    """
    Render the home page with featured destinations and packages.

    Args:
        request: HTTP request object

    Returns:
        Rendered home template with featured content
    """
    try:
        destinations = Destination.objects.all()[:FEATURED_DESTINATIONS_COUNT]
        featured_packages = TourPackage.objects.all()[:FEATURED_PACKAGES_COUNT]
        logger.info("Home page loaded successfully")
    except Exception as e:
        logger.error(f"Error loading home page: {e}")
        messages.error(request, "Error loading featured content")
        destinations = []
        featured_packages = []

    return render(
        request,
        "travel/home_new.html",
        {
            "destinations": destinations,
            "packages": featured_packages,
        },
    )

def destination_list(request: HttpRequest) -> HttpResponse:
    """
    Display paginated list of all destinations.

    Args:
        request: HTTP request object

    Returns:
        Rendered destination list template with pagination
    """
    destinations = Destination.objects.all()
    paginator = Paginator(destinations, ITEMS_PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    logger.info(f"Destinations list accessed - Page: {page_number}")
    return render(request, "travel/destination_list_new.html", {"destinations": page_obj, "page_obj": page_obj})

def destination_detail(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Display detailed view of a specific destination with related packages.

    Args:
        request: HTTP request object
        pk: Primary key of the destination

    Returns:
        Rendered destination detail template
    """
    destination = get_object_or_404(Destination, pk=pk)
    packages = destination.packages.all()

    logger.info(f"Destination detail accessed - ID: {pk}")
    return render(
        request,
        "travel/destination_detail.html",
        {"destination": destination, "packages": packages},
    )

def package_list(request: HttpRequest) -> HttpResponse:
    """
    Display paginated list of tour packages with filtering options.

    Supports filtering by:
    - difficulty: Package difficulty level
    - min_price & max_price: Price range
    - duration: Package duration

    Args:
        request: HTTP request object

    Returns:
        Rendered package list template with filtered and paginated results
    """
    packages = TourPackage.objects.all()

    # Apply difficulty filter
    difficulty = request.GET.get("difficulty")
    if difficulty:
        packages = packages.filter(difficulty=difficulty)

    # Apply price range filter
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    if min_price and max_price:
        try:
            packages = packages.filter(
                price__gte=float(min_price), price__lte=float(max_price)
            )
        except (ValueError, TypeError) as e:
            logger.warning(f"Invalid price filter values: {e}")
            messages.warning(request, "Invalid price range provided")

    # Apply duration filter
    duration = request.GET.get("duration")
    if duration:
        packages = packages.filter(duration=duration)

    # Paginate results
    paginator = Paginator(packages, ITEMS_PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    logger.info(
        f"Package list accessed - Filters: difficulty={difficulty}, "
        f"price={min_price}-{max_price}, duration={duration}"
    )

    return render(request, "travel/package_list_new.html", {"packages": page_obj, "page_obj": page_obj})

def package_detail(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Display detailed view of a tour package with booking and review forms.

    Handles both:
    - Booking form submission
    - Review form submission

    Args:
        request: HTTP request object
        pk: Primary key of the package

    Returns:
        Rendered package detail template with forms and reviews
    """
    package = get_object_or_404(TourPackage, pk=pk)
    reviews = package.reviews.all()
    booking_form = BookingForm()
    review_form = ReviewForm()

    if request.method == "POST":
        try:
            # Handle booking submission
            if "booking_submit" in request.POST:
                booking_form = BookingForm(request.POST)
                if booking_form.is_valid():
                    booking = booking_form.save(commit=False)
                    booking.package = package
                    booking.save()
                    logger.info(f"Booking created - Package ID: {pk}, Booking ID: {booking.pk}")
                    messages.success(
                        request, "Your booking has been submitted successfully!"
                    )
                    return redirect("booking_confirmation", pk=booking.pk)
                else:
                    logger.warning(f"Invalid booking form for package {pk}")

            # Handle review submission
            elif "review_submit" in request.POST:
                review_form = ReviewForm(request.POST)
                if review_form.is_valid():
                    review = review_form.save(commit=False)
                    review.package = package
                    review.save()
                    logger.info(f"Review created for package {pk}")
                    messages.success(request, "Thank you for your review!")
                    return redirect("package_detail", pk=package.pk)
                else:
                    logger.warning(f"Invalid review form for package {pk}")
        except Exception as e:
            logger.error(f"Error processing form for package {pk}: {e}")
            messages.error(request, "An error occurred while processing your request")

    logger.info(f"Package detail accessed - ID: {pk}")
    return render(
        request,
        "travel/package_detail.html",
        {
            "package": package,
            "reviews": reviews,
            "booking_form": booking_form,
            "review_form": review_form,
        },
    )

def booking_confirmation(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Display booking confirmation details.

    Args:
        request: HTTP request object
        pk: Primary key of the booking

    Returns:
        Rendered booking confirmation template
    """
    booking = get_object_or_404(Booking, pk=pk)
    logger.info(f"Booking confirmation accessed - Booking ID: {pk}")
    return render(request, "travel/booking_confirmation.html", {"booking": booking})

def search_packages(request: HttpRequest) -> HttpResponse:
    """
    Search for packages by query string.

    Searches across package title, description, and destination name.

    Args:
        request: HTTP request object with 'q' GET parameter

    Returns:
        Rendered search results template with matching packages
    """
    query = request.GET.get("q", "").strip()
    packages = TourPackage.objects.none()

    if query:
        try:
            packages = TourPackage.objects.filter(
                models.Q(title__icontains=query)
                | models.Q(description__icontains=query)
                | models.Q(destination__name__icontains=query)
            ).distinct()
            logger.info(f"Search executed - Query: '{query}', Results: {packages.count()}")
        except Exception as e:
            logger.error(f"Error during package search: {e}")
            messages.error(request, "An error occurred during search")
    else:
        logger.debug("Empty search query provided")

    return render(
        request,
        "travel/search_results.html",
        {"packages": packages, "query": query},
    )

def login_view(request: HttpRequest) -> HttpResponse:
    """
    Handle user login.

    GET: Display login form
    POST: Authenticate user and redirect to home on success

    Args:
        request: HTTP request object

    Returns:
        Rendered login template or redirect to home
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    logger.info(f"User logged in successfully: {username}")
                    messages.success(request, f"Welcome back, {username}!")
                    return redirect("travel:home")
            except Exception as e:
                logger.error(f"Login error for user: {e}")
                messages.error(request, "An error occurred during login")
        else:
            logger.warning(f"Failed login attempt with invalid credentials")
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, "travel/login.html", {"form": form})

def register_view(request: HttpRequest) -> HttpResponse:
    """
    Handle new user registration.

    GET: Display registration form
    POST: Create new user account and log them in

    Args:
        request: HTTP request object

    Returns:
        Rendered registration template or redirect to home
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                logger.info(f"New user registered successfully: {user.username}")
                messages.success(
                    request,
                    f"Account created successfully! Welcome, {user.username}!",
                )
                return redirect("travel:home")
            except Exception as e:
                logger.error(f"Error during user registration: {e}")
                messages.error(request, "An error occurred during registration")
        else:
            logger.warning("Registration form validation failed")
            # Form errors will be displayed in the template
    else:
        form = UserCreationForm()

    return render(request, "travel/register.html", {"form": form})
