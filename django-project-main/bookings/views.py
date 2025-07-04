from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.db.models import Q
from .models import Tour, TourDate, Booking, Payment
from .forms import BookingForm, PaymentForm
import stripe
from accounts.models import Wishlist
import paypalrestsdk
from django.views.decorators.csrf import csrf_exempt
import re
from django.utils import timezone
from django.template.loader import get_template
from xhtml2pdf import pisa
import uuid
from django.views.generic import View

stripe.api_key = settings.STRIPE_SECRET_KEY

# Configure PayPal
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_SECRET
})

def tour_list(request):
    """Display a list of all available tours."""
    tours = Tour.objects.filter(is_active=True)
    
    # Filter by search query if provided
    query = request.GET.get('q')
    if query:
        tours = tours.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(destination__name__icontains=query)
        )
    
    # Filter by category if provided
    category = request.GET.get('category')
    if category:
        tours = tours.filter(categories__slug=category)
    
    # Filter by price range if provided
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        tours = tours.filter(price__gte=min_price)
    if max_price:
        tours = tours.filter(price__lte=max_price)
    
    context = {
        'tours': tours,
        'query': query,
        'category': category,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'bookings/tour_list.html', context)

def tour_search(request):
    # Handle tour search logic here
    return render(request, 'bookings/tour_search.html')

def tour_detail(request, slug):
    """Display details of a specific tour."""
    tour = get_object_or_404(Tour, slug=slug, is_active=True)
    is_in_wishlist = False
    
    if request.user.is_authenticated:
        is_in_wishlist = Wishlist.objects.filter(user=request.user, tour=tour).exists()
    
    available_dates = TourDate.objects.filter(tour=tour, available_seats__gt=0)
    context = {
        'tour': tour,
        'is_in_wishlist': is_in_wishlist,
        'available_dates': available_dates
    }
    return render(request, 'bookings/tour_detail.html', context)

@login_required
def create_booking(request, slug):
    """Create a new booking for a tour."""
    tour = get_object_or_404(Tour, slug=slug, is_active=True)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.tour = tour
            booking.user = request.user
            booking.save()
            messages.success(request, 'Booking created successfully!')
            return redirect('bookings:booking_detail', booking_id=booking.id)
    else:
        form = BookingForm()
    
    context = {
        'tour': tour,
        'form': form,
    }
    return render(request, 'bookings/create_booking.html', context)

@login_required
def my_bookings(request):
    """Display all bookings for the current user."""
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})

@login_required
def booking_detail(request, booking_id):
    """Display details of a specific booking."""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    context = {
        'booking': booking,
    }
    return render(request, 'bookings/booking_detail.html', context)

@login_required
def cancel_booking(request, booking_id):
    """Cancel a booking."""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.can_be_cancelled():
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Booking cancelled successfully!')
    else:
        messages.error(request, 'This booking cannot be cancelled.')
    
    return redirect('bookings:booking_detail', booking_id=booking.id)

@login_required
def process_payment(request, booking_id):
    """Process payment for a booking."""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.booking = booking
            payment.save()
            return redirect('bookings:payment_success', booking_id=booking.id)
    else:
        form = PaymentForm()
    
    context = {
        'booking': booking,
        'form': form,
    }
    return render(request, 'bookings/process_payment.html', context)

@login_required
def payment_success(request, booking_id):
    """Display payment success page."""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    context = {
        'booking': booking,
    }
    return render(request, 'bookings/payment_success.html', context)

@login_required
def checkout(request, reference):
    booking = get_object_or_404(Booking, booking_reference=reference, user=request.user)
    
    if request.method == 'POST':
        try:
            # Create Stripe checkout session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(booking.total_price * 100),
                        'product_data': {
                            'name': booking.tour_date.tour.name,
                        },
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri(f'/booking/{booking.booking_reference}/'),
                cancel_url=request.build_absolute_uri(f'/booking/{booking.booking_reference}/'),
            )
            return JsonResponse({'stripe_session_id': checkout_session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return render(request, 'bookings/checkout.html', {'booking': booking})

def stripe_webhook(request):
    # Handle Stripe webhook events here
    return JsonResponse({'status': 'success'})

@login_required
def book_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.tour = tour
            booking.booking_reference = str(uuid.uuid4().hex[:8].upper())
            booking.base_price = tour.price * booking.participants
            booking.gst_amount = booking.base_price * 0.05  # 5% GST
            booking.sgst_amount = booking.base_price * 0.05  # 5% SGST
            booking.total_amount = booking.base_price + booking.gst_amount + booking.sgst_amount
            booking.save()
            
            messages.success(request, 'Booking created successfully!')
            return redirect('bookings:payment', booking_id=booking.id)
    else:
        form = BookingForm()
    
    context = {
        'form': form,
        'tour': tour,
    }
    return render(request, 'bookings/booking_form.html', context)

@login_required
def payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        
        # Create payment record
        payment = Payment.objects.create(
            booking=booking,
            amount=booking.total_amount,
            payment_method=payment_method,
            status='completed'
        )
        
        # Update booking status
        booking.status = 'confirmed'
        booking.payment_method = payment_method
        booking.transaction_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
        booking.save()
        
        messages.success(request, 'Payment successful!')
        return redirect('bookings:booking_confirmation', booking_id=booking.id)
    
    context = {
        'booking': booking,
    }
    return render(request, 'bookings/payment.html', context)

@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'bookings/booking_confirmation.html', {'booking': booking})

@login_required
def download_invoice(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    template = get_template('bookings/invoice_pdf.html')
    context = {'booking': booking}
    html = template.render(context)
    
    # Create PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{booking.booking_reference}.pdf"'
    
    # Generate PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)
    
    return response

@csrf_exempt
def paypal_webhook(request):
    if request.method == 'POST':
        try:
            # Verify webhook signature
            # Note: In production, you should verify the webhook signature
            # using PayPal's webhook verification
            
            payload = request.POST
            event_type = payload.get('event_type')
            
            if event_type == 'PAYMENT.SALE.COMPLETED':
                payment_id = payload.get('resource', {}).get('parent_payment')
                
                # Update booking status
                try:
                    booking = Booking.objects.get(payment_id=payment_id)
                    booking.status = 'confirmed'
                    booking.save()
                except Booking.DoesNotExist:
                    return HttpResponse(status=404)
                    
            return HttpResponse(status=200)
            
        except Exception as e:
            return HttpResponse(status=400)
    
    return HttpResponse(status=400)

@login_required
def payment_cancel(request, booking_id):
    """Handle cancelled PayPal payments."""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    messages.warning(request, "Payment was cancelled. You can try again or contact support.")
    return redirect('bookings:booking_detail', booking_id=booking.id)

@login_required
def create_payment_intent(request, booking_id):
    """Create a Stripe PaymentIntent for a booking."""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    try:
        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            amount=int(booking.total_price * 100),  # Convert to cents
            currency='inr',
            payment_method_types=['card'],
            metadata={
                'booking_id': booking.id,
                'user_id': request.user.id
            }
        )
        
        return JsonResponse({
            'clientSecret': intent.client_secret
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

class PaymentView(View):
    template_name = 'bookings/tour_payment.html'
    
    def get(self, request, *args, **kwargs):
        tours = Tour.objects.filter(is_active=True)
        context = {
            'tours': tours
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        # Handle payment processing here
        # This is where you would integrate with a payment gateway
        # For now, we'll just show a success message
        return render(request, 'bookings/payment_success.html')