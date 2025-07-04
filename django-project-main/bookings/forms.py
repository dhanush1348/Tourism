from django import forms
from .models import Booking, Payment
from django.utils import timezone

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'full_name',
            'email',
            'phone',
            'participants',
            'payment_method',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'participants': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_start_date(self):
        start_date = self.cleaned_data['start_date']
        if start_date < timezone.now().date():
            raise forms.ValidationError('Please select a future date.')
        return start_date
    
    def clean_num_people(self):
        num_people = self.cleaned_data['num_people']
        tour = self.instance.tour if self.instance and self.instance.pk else None
        if tour and num_people > tour.group_size_max:
            raise forms.ValidationError(f'Maximum group size is {tour.group_size_max} people.')
        return num_people

    def clean(self):
        cleaned_data = super().clean()
        participants = cleaned_data.get('participants')
        if participants:
            cleaned_data['num_people'] = participants
        return cleaned_data

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_method', 'transaction_id']
        widgets = {
            'payment_method': forms.Select(choices=[
                ('card', 'Credit/Debit Card'),
                ('upi', 'UPI'),
                ('net_banking', 'Net Banking'),
            ]),
        } 
from django import forms

class BookingForm(forms.Form):
    full_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your full name'
    }))
    
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'your@email.com'
    }))
    
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '+1 234 567 8900'
    }))
    
    participants = forms.IntegerField(min_value=1, max_value=10, widget=forms.NumberInput(attrs={
        'class': 'form-control'
    }))
    
    special_requests = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 3,
        'placeholder': 'Any special requirements or requests...'
    }))