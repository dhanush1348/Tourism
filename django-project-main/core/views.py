from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Avg, Q
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.http import HttpResponse
from .models import Destination, Category
from bookings.models import Tour
from blog.models import Post
from django.core.paginator import Paginator

def home(request):
    featured_destinations = Destination.objects.filter(is_active=True)[:6]
    featured_tours = Tour.objects.filter(is_active=True)[:6]
    categories = Category.objects.filter(is_active=True)
    latest_posts = Post.objects.filter(status='published').order_by('-published_at')[:3]
    
    context = {
        'featured_destinations': featured_destinations,
        'featured_tours': featured_tours,
        'categories': categories,
        'latest_posts': latest_posts,
    }
    return render(request, 'core/home.html', context)

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Send email
        email_message = f"""
        Name: {name}
        Email: {email}
        Subject: {subject}
        Message:
        {message}
        """
        
        try:
            send_mail(
                subject=f'Contact Form: {subject}',
                message=email_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            if request.htmx:
                return HttpResponse('<div class="alert alert-success">Thank you for your message! We will get back to you soon.</div>')
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
        except Exception as e:
            if request.htmx:
                return HttpResponse('<div class="alert alert-danger">Sorry, there was an error sending your message. Please try again later.</div>')
            messages.error(request, 'Sorry, there was an error sending your message. Please try again later.')
    
    context = {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, 'core/contact.html', context)

def destination_list(request):
    # Get all categories with destination counts
    categories = Category.objects.annotate(
        destination_count=Count('tour__destination', distinct=True)
    ).order_by('name')
    
    # Get selected category from query params
    selected_category_slug = request.GET.get('category')
    selected_category = None
    destinations = Destination.objects.filter(is_active=True)
    
    if selected_category_slug:
        selected_category = get_object_or_404(Category, slug=selected_category_slug)
        destinations = destinations.filter(tour__category=selected_category).distinct()
    
    # Search functionality
    search_query = request.GET.get('q')
    if search_query:
        destinations = destinations.filter(
            Q(name__icontains=search_query) |
            Q(city__icontains=search_query) |
            Q(country__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Filter by featured destinations (using is_active instead)
    featured_only = request.GET.get('featured')
    if featured_only:
        destinations = destinations.filter(is_active=True)
    
    # Filter by price range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        destinations = destinations.filter(min_price__gte=float(min_price))
    if max_price:
        destinations = destinations.filter(min_price__lte=float(max_price))
    
    # Sort destinations
    sort_by = request.GET.get('sort')
    if sort_by == 'price_asc':
        destinations = destinations.order_by('min_price')
    elif sort_by == 'price_desc':
        destinations = destinations.order_by('-min_price')
    elif sort_by == 'name':
        destinations = destinations.order_by('name')
    else:
        destinations = destinations.order_by('-created_at', 'name')
    
    # Pagination
    paginator = Paginator(destinations, 12)  # Show 12 destinations per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'destinations': page_obj,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': search_query,
        'featured_only': featured_only,
        'min_price': min_price,
        'max_price': max_price,
        'sort_by': sort_by,
    }
    return render(request, 'core/destination_list.html', context)

def destination_detail(request, slug):
    destination = get_object_or_404(Destination, slug=slug)
    
    # Get related destinations (same category, excluding current)
    related_destinations = Destination.objects.filter(
        category=destination.category
    ).exclude(id=destination.id)[:3]
    
    # Get available tours for this destination
    tours = destination.tours.filter(is_active=True)
    
    context = {
        'destination': destination,
        'related_destinations': related_destinations,
        'tours': tours,
    }
    return render(request, 'core/destination_detail.html', context)

def faq(request):
    """Display the FAQ page."""
    return render(request, 'core/faq.html')

def team(request):
    """Display the team page."""
    team_members = [
        {
            'name': 'Tharun',
            'position': 'Founder & CEO',
            'bio': 'With a passion for travel and technology, Tharun leads our team with innovative ideas and strategic vision.',
            'image': 'team/tharun.jpg',
            'specialization': 'Technology & Innovation'
        },
        {
            'name': 'Adithya',
            'position': 'Operations Director',
            'bio': 'Adithya ensures every tour runs smoothly with his exceptional organizational skills and attention to detail.',
            'image': 'team/adithya.jpg',
            'specialization': 'Tour Operations'
        },
        {
            'name': 'Dhanush',
            'position': 'Marketing Director',
            'bio': 'Dhanush brings destinations to life through creative marketing strategies and digital campaigns.',
            'image': 'team/dhanush.jpg',
            'specialization': 'Digital Marketing'
        },
        {
            'name': 'Lokesh',
            'position': 'Adventure Specialist',
            'bio': 'Lokesh curates thrilling adventure experiences and ensures safety in all our adventure tours.',
            'image': 'team/lokesh.jpg',
            'specialization': 'Adventure Tourism'
        },
        {
            'name': 'Sanjana',
            'position': 'Cultural Experience Curator',
            'bio': 'Sanjana designs authentic cultural experiences that connect travelers with local traditions.',
            'image': 'team/sanjana.jpg',
            'specialization': 'Cultural Tourism'
        },
        {
            'name': 'Madhu',
            'position': 'Customer Experience Manager',
            'bio': 'Madhu ensures every traveler has a memorable experience with personalized service.',
            'image': 'team/madhu.jpg',
            'specialization': 'Customer Relations'
        },
        {
            'name': 'Sunitha',
            'position': 'Sustainability Coordinator',
            'bio': 'Sunitha leads our eco-friendly initiatives and sustainable tourism practices.',
            'image': 'team/sunitha.jpg',
            'specialization': 'Sustainable Tourism'
        }
    ]
    
    # Create special posts for each team member
    special_posts = [
        {
            'title': 'The Future of Travel Technology',
            'author': 'Tharun',
            'date': '2024-04-15',
            'content': 'Exploring how technology is transforming the travel industry...',
            'image': 'blog/tech-travel.jpg'
        },
        {
            'title': 'Behind the Scenes: Tour Operations',
            'author': 'Adithya',
            'date': '2024-04-10',
            'content': 'A day in the life of our operations team...',
            'image': 'blog/operations.jpg'
        },
        {
            'title': 'Digital Marketing in Travel',
            'author': 'Dhanush',
            'date': '2024-04-05',
            'content': 'How we reach travelers in the digital age...',
            'image': 'blog/digital-marketing.jpg'
        },
        {
            'title': 'Adventure Tourism Safety',
            'author': 'Lokesh',
            'date': '2024-03-28',
            'content': 'Essential safety tips for adventure travelers...',
            'image': 'blog/adventure-safety.jpg'
        },
        {
            'title': 'Cultural Immersion Experiences',
            'author': 'Sanjana',
            'date': '2024-03-20',
            'content': 'Creating authentic cultural connections...',
            'image': 'blog/cultural-immersion.jpg'
        },
        {
            'title': 'Customer Service Excellence',
            'author': 'Madhu',
            'date': '2024-03-15',
            'content': 'The art of creating memorable travel experiences...',
            'image': 'blog/customer-service.jpg'
        },
        {
            'title': 'Sustainable Tourism Practices',
            'author': 'Sunitha',
            'date': '2024-03-10',
            'content': 'How we\'re making travel more sustainable...',
            'image': 'blog/sustainability.jpg'
        }
    ]
    
    context = {
        'team_members': team_members,
        'special_posts': special_posts
    }
    return render(request, 'core/team.html', context)
