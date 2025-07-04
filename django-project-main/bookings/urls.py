from django.urls import path
from . import views
from .views import PaymentView

app_name = 'bookings'

urlpatterns = [
    path('tours/', views.tour_list, name='tour_list'),
    path('tour/<int:tour_id>/', views.tour_detail, name='tour_detail'),
    path('', views.my_bookings, name='my_bookings'),
    path('book/<int:tour_id>/', views.book_tour, name='book_tour'),
    path('payment/<int:booking_id>/', views.payment, name='payment'),
    path('confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('invoice/<int:booking_id>/', views.download_invoice, name='download_invoice'),
    path('stripe-webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('paypal-webhook/', views.paypal_webhook, name='paypal_webhook'),
    path('tour-payment/', PaymentView.as_view(), name='tour_payment'),
    path('booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),
] 