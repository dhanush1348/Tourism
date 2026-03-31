from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

class Destination(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='destinations/')
    
    def __str__(self):
        return self.name

class TourPackage(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('moderate', 'Moderate'),
        ('challenging', 'Challenging'),
    ]
    
    title = models.CharField(max_length=200)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='packages')
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    duration = models.IntegerField(help_text='Duration in days')
    max_participants = models.IntegerField(default=15)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='moderate')
    included_services = models.TextField(help_text='Services included in the package')
    image = models.ImageField(upload_to='packages/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.destination.name}"

    class Meta:
        ordering = ['-created_at']

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='bookings')
    number_of_participants = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    booking_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    special_requirements = models.TextField(blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user_name} - {self.package.title}"
    
    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.package.price * self.number_of_participants
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='reviews')
    user_name = models.CharField(max_length=100)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user_name} - {self.package.title} - {self.rating} stars"

    class Meta:
        ordering = ['-created_at']
