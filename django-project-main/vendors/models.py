from django.db import models
from django.conf import settings
from django.utils.text import slugify
from core.models import Review

class Vendor(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('suspended', 'Suspended'),
        ('rejected', 'Rejected'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    logo = models.ImageField(upload_to='vendor_logos/')
    cover_image = models.ImageField(upload_to='vendor_covers/')
    address = models.TextField()
    registration_number = models.CharField(max_length=50)
    tax_number = models.CharField(max_length=50)
    website = models.URLField(blank=True)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    
    # Documents
    business_certificate = models.FileField(upload_to='vendor_documents/')
    tax_certificate = models.FileField(upload_to='vendor_documents/')
    insurance_certificate = models.FileField(upload_to='vendor_documents/')
    
    # Verification
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_featured = models.BooleanField(default=False)
    verification_notes = models.TextField(blank=True)
    
    # Social Media
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    
    # Bank Details (encrypted in production)
    bank_name = models.CharField(max_length=100)
    bank_account_name = models.CharField(max_length=100)
    bank_account_number = models.CharField(max_length=50)
    bank_routing_number = models.CharField(max_length=50)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.company_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.company_name

    def get_rating(self):
        reviews = self.vendorreview_set.all()
        if not reviews:
            return 0
        return sum(review.rating for review in reviews) / len(reviews)

class VendorReview(Review):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['user', 'vendor']

class VendorDocument(models.Model):
    DOCUMENT_TYPES = [
        ('business', 'Business Certificate'),
        ('tax', 'Tax Certificate'),
        ('insurance', 'Insurance Certificate'),
        ('other', 'Other'),
    ]

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to='vendor_documents/')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    verification_notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.vendor.company_name} - {self.get_document_type_display()}"
