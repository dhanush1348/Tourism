from django.contrib import admin
from .models import Tour, TourDate, TourReview, Booking, Payment

class TourDateInline(admin.TabularInline):
    model = TourDate
    extra = 1

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'duration_days', 'price', 'is_active')
    list_filter = ('is_active', 'destination', 'categories')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    inlines = [TourDateInline]
    filter_horizontal = ('categories', 'amenities')

@admin.register(TourDate)
class TourDateAdmin(admin.ModelAdmin):
    list_display = ('tour', 'start_date', 'end_date', 'available_seats', 'is_guaranteed')
    list_filter = ('is_guaranteed', 'start_date')
    search_fields = ('tour__name',)
    date_hierarchy = 'start_date'

@admin.register(TourReview)
class TourReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'tour__name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_reference', 'user', 'tour', 'participants', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['booking_reference', 'user__email', 'tour__name']
    readonly_fields = ['booking_reference', 'created_at', 'updated_at']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['booking', 'amount', 'payment_method', 'status', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['booking__booking_reference', 'transaction_id']
    readonly_fields = ['created_at']
