"""
Health check and SEO views for the travel app.
"""

import logging
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from .models import TourPackage, Destination, Booking

logger = logging.getLogger(__name__)


@require_http_methods(["GET"])
def health_check(request):
    """
    Health check endpoint for monitoring and load balancers.
    
    Returns a JSON response with the application status and dependencies.
    Used by Docker health checks and monitoring systems.
    """
    try:
        # Check database connectivity
        destination_count = Destination.objects.count()
        package_count = TourPackage.objects.count()
        
        # Check recent bookings (within last 24 hours)
        from datetime import timedelta
        recent_bookings = Booking.objects.filter(
            created_at__gte=timezone.now() - timedelta(hours=24)
        ).count()
        
        health_status = {
            'status': 'healthy',
            'timestamp': timezone.now().isoformat(),
            'database': 'connected',
            'metrics': {
                'destinations': destination_count,
                'packages': package_count,
                'recent_bookings_24h': recent_bookings,
            }
        }
        logger.info("Health check: healthy")
        return JsonResponse(health_status)
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JsonResponse(
            {
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': timezone.now().isoformat()
            },
            status=503
        )


@require_http_methods(["GET"])
def sitemap(request):
    """
    Generate XML sitemap for SEO.
    
    Returns a sitemap.xml file with all important URLs for search engines.
    """
    try:
        from django.contrib.sites.shortcuts import get_current_site
        current_site = request.build_absolute_uri('/')
        
        xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        
        # Add static pages
        static_urls = [
            ('/', 'daily', '1.0'),
            ('/destination_list/', 'weekly', '0.9'),
            ('/package_list/', 'weekly', '0.9'),
            ('/contact/', 'monthly', '0.8'),
        ]
        
        for url, freq, priority in static_urls:
            xml_content += f'  <url>\n'
            xml_content += f'    <loc>{current_site.rstrip("/")}{url}</loc>\n'
            xml_content += f'    <changefreq>{freq}</changefreq>\n'
            xml_content += f'    <priority>{priority}</priority>\n'
            xml_content += f'  </url>\n'
        
        # Add dynamic destination pages
        destinations = Destination.objects.all()
        for destination in destinations:
            xml_content += f'  <url>\n'
            xml_content += f'    <loc>{current_site.rstrip("/")}/destination/{destination.pk}/</loc>\n'
            xml_content += f'    <changefreq>weekly</changefreq>\n'
            xml_content += f'    <priority>0.8</priority>\n'
            xml_content += f'  </url>\n'
        
        # Add dynamic package pages
        packages = TourPackage.objects.all()
        for package in packages:
            xml_content += f'  <url>\n'
            xml_content += f'    <loc>{current_site.rstrip("/")}/package/{package.pk}/</loc>\n'
            xml_content += f'    <lastmod>{package.created_at.isoformat()}</lastmod>\n'
            xml_content += f'    <changefreq>weekly</changefreq>\n'
            xml_content += f'    <priority>0.7</priority>\n'
            xml_content += f'  </url>\n'
        
        xml_content += '</urlset>'
        
        logger.info("Sitemap generated successfully")
        return HttpResponse(xml_content, content_type='application/xml')
        
    except Exception as e:
        logger.error(f"Sitemap generation failed: {e}")
        return HttpResponse(
            '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>',
            content_type='application/xml',
            status=500
        )


@require_http_methods(["GET"])
def robots_txt(request):
    """
    Generate robots.txt for search engine crawlers.
    
    Instructs search engines on which pages to crawl and block.
    """
    content = """# Robots.txt for Wanderlust Travel
User-agent: *
Allow: /
Disallow: /admin/
Disallow: /auth/
Disallow: /search/
Disallow: /*.json$
Disallow: /api/
Disallow: /user/

# Allow crawling of static files
Allow: /static/
Allow: /media/

# Sitemaps
Sitemap: https://www.wanderlust.com/sitemap.xml

# Crawl delay
Crawl-delay: 1

# User agents
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /
"""
    return HttpResponse(content, content_type='text/plain')
