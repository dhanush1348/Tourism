from django.urls import path
from . import views, views_seo, api
from django.contrib.auth import views as auth_views

app_name = 'travel'

urlpatterns = [
    # Landing page (premium React-powered homepage)
    path('', api.landing_view, name='home'),
    
    # Destinations & Packages
    path('destinations/', views.destination_list, name='destination_list'),
    path('destinations/<int:pk>/', views.destination_detail, name='destination_detail'),
    path('packages/', views.package_list, name='package_list'),
    path('packages/<int:pk>/', views.package_detail, name='package_detail'),
    path('booking/<int:pk>/confirmation/', views.booking_confirmation, name='booking_confirmation'),
    path('search/', views.search_packages, name='search_packages'),
    
    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='travel:home'), name='logout'),
    
    # API Endpoints
    path('api/chat/', api.chat_view, name='api_chat'),
    path('api/bookings/', api.booking_view, name='api_bookings'),
    
    # SEO & Health Check URLs
    path('health/', views_seo.health_check, name='health_check'),
    path('sitemap.xml', views_seo.sitemap, name='sitemap'),
    path('robots.txt', views_seo.robots_txt, name='robots_txt'),
]
