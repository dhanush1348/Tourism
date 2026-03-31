from django.contrib import admin
from .models import Destination, TourPackage, Booking, Review

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name', 'location')

@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'destination', 'price', 'duration', 'difficulty')
    list_filter = ('difficulty', 'destination')
    search_fields = ('title', 'description')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'package', 'booking_date', 'status', 'total_price')
    list_filter = ('status', 'booking_date')
    search_fields = ('user_name', 'email')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'package', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user_name', 'comment')
