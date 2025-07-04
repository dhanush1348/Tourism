from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Vendor, VendorDocument
from bookings.models import Tour, Booking

def vendor_list(request):
    vendors = Vendor.objects.filter(status='approved')
    return render(request, 'vendors/vendor_list.html', {'vendors': vendors})

@login_required
def vendor_register(request):
    if request.method == 'POST':
        # Handle vendor registration logic here
        messages.success(request, 'Your vendor application has been submitted.')
        return redirect('vendors:dashboard')
    return render(request, 'vendors/vendor_register.html')

@login_required
def vendor_dashboard(request):
    vendor = get_object_or_404(Vendor, user=request.user)
    tours = Tour.objects.filter(vendor=vendor)
    bookings = Booking.objects.filter(tour_date__tour__vendor=vendor)
    return render(request, 'vendors/dashboard.html', {
        'vendor': vendor,
        'tours': tours,
        'bookings': bookings
    })

@login_required
def vendor_tours(request):
    vendor = get_object_or_404(Vendor, user=request.user)
    tours = Tour.objects.filter(vendor=vendor)
    return render(request, 'vendors/tours.html', {'tours': tours})

@login_required
def tour_add(request):
    if request.method == 'POST':
        # Handle tour creation logic here
        messages.success(request, 'Tour created successfully.')
        return redirect('vendors:tours')
    return render(request, 'vendors/tour_add.html')

@login_required
def tour_edit(request, slug):
    vendor = get_object_or_404(Vendor, user=request.user)
    tour = get_object_or_404(Tour, slug=slug, vendor=vendor)
    if request.method == 'POST':
        # Handle tour update logic here
        messages.success(request, 'Tour updated successfully.')
        return redirect('vendors:tours')
    return render(request, 'vendors/tour_edit.html', {'tour': tour})

@login_required
def vendor_bookings(request):
    vendor = get_object_or_404(Vendor, user=request.user)
    bookings = Booking.objects.filter(tour_date__tour__vendor=vendor)
    return render(request, 'vendors/bookings.html', {'bookings': bookings})

@login_required
def vendor_profile(request):
    vendor = get_object_or_404(Vendor, user=request.user)
    if request.method == 'POST':
        # Handle vendor profile update logic here
        messages.success(request, 'Profile updated successfully.')
        return redirect('vendors:profile')
    return render(request, 'vendors/profile.html', {'vendor': vendor})

@login_required
def vendor_documents(request):
    vendor = get_object_or_404(Vendor, user=request.user)
    documents = VendorDocument.objects.filter(vendor=vendor)
    if request.method == 'POST':
        # Handle document upload logic here
        messages.success(request, 'Document uploaded successfully.')
        return redirect('vendors:documents')
    return render(request, 'vendors/documents.html', {'documents': documents})

def vendor_detail(request, slug):
    vendor = get_object_or_404(Vendor, slug=slug, status='approved')
    tours = Tour.objects.filter(vendor=vendor, is_active=True)
    return render(request, 'vendors/vendor_detail.html', {
        'vendor': vendor,
        'tours': tours
    })
