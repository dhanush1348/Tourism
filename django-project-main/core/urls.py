from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    
    # About page
    path('about/', views.about, name='about'),
    
    # Contact page
    path('contact/', views.contact, name='contact'),
    
    # Destinations
    path('destinations/', views.destination_list, name='destination_list'),
    path('destinations/<slug:slug>/', views.destination_detail, name='destination_detail'),
    
    # FAQ page
    path('faq/', views.faq, name='faq'),
    
    # Team page
    path('team/', views.team, name='team'),
] 