from django import forms
from django.utils import timezone
from .models import Booking, Review

class BookingForm(forms.ModelForm):
    booking_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'min': timezone.now().date().isoformat()})
    )
    
    class Meta:
        model = Booking
        fields = ['user_name', 'email', 'phone', 'number_of_participants', 
                 'booking_date', 'special_requirements']
        widgets = {
            'special_requirements': forms.Textarea(attrs={'rows': 4}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['user_name', 'rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
        }
