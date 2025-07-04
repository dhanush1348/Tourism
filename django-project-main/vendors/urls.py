from django.urls import path
from . import views

app_name = 'vendors'

urlpatterns = [
    path('', views.vendor_list, name='list'),
    path('register/', views.vendor_register, name='register'),
    path('dashboard/', views.vendor_dashboard, name='dashboard'),
    path('tours/', views.vendor_tours, name='tours'),
    path('tours/add/', views.tour_add, name='tour_add'),
    path('tours/<slug:slug>/edit/', views.tour_edit, name='tour_edit'),
    path('bookings/', views.vendor_bookings, name='bookings'),
    path('profile/', views.vendor_profile, name='profile'),
    path('documents/', views.vendor_documents, name='documents'),
    path('<slug:slug>/', views.vendor_detail, name='detail'),
] 