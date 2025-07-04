from django.db import models
from django.utils.text import slugify
from django.conf import settings
from core.models import Destination, Category, Amenity, Review
from tours.models import Tour

class Tour(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    amenities = models.ManyToManyField(Amenity)
    duration_days = models.PositiveIntegerField()
    duration_nights = models.PositiveIntegerField()
    group_size_min = models.PositiveIntegerField()
    group_size_max = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    featured_image = models.ImageField(upload_to='tours/')
    gallery_images = models.JSONField(default=list)  # List of image URLs
    included_services = models.JSONField(default=list)
    excluded_services = models.JSONField(default=list)
    itinerary = models.JSONField(default=dict)  # Day by day itinerary
    meeting_point = models.TextField()
    vendor = models.ForeignKey('vendors.Vendor', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_rating(self):
        reviews = self.tourreview_set.all()
        if not reviews:
            return 0
        return sum(review.rating for review in reviews) / len(reviews)

    def get_availability_color(self):
        if self.is_active and self.group_size_max > 0:
            return 'success'
        return 'danger'

    def get_availability_display(self):
        if self.is_active and self.group_size_max > 0:
            return 'Available'
        return 'Not Available'

    @property
    def gst_amount(self):
        return self.price * 0.05  # 5% GST

    @property
    def sgst_amount(self):
        return self.price * 0.05  # 5% SGST

    @property
    def total_amount(self):
        return self.price + self.gst_amount + self.sgst_amount

class TourDate(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    available_seats = models.PositiveIntegerField()
    price_modifier = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)
    is_guaranteed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return f"{self.tour.name} - {self.start_date}"

class TourReview(Review):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    photos = models.JSONField(default=list)  # List of photo URLs
    
    class Meta:
        unique_together = ['user', 'tour']

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('paypal', 'PayPal'),
        ('upi', 'UPI'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    booking_reference = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100, default='')
    email = models.EmailField(default='')
    phone = models.CharField(max_length=15, default='')
    participants = models.PositiveIntegerField(default=1)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    gst_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sgst_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='credit_card')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.booking_reference} - {self.tour.name}"
    
    class Meta:
        ordering = ['-created_at']

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('paypal', 'PayPal'),
        ('upi', 'UPI'),
    ]
    
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='credit_card')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.booking.booking_reference} - {self.amount}"
    
    class Meta:
        ordering = ['-created_at']