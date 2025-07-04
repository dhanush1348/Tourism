from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Tour(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    max_participants = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('tours:detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at'] 