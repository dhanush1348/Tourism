# Tours & Travels Booking System

A comprehensive real-time booking system for tours and travel packages built with Django.

## Features

- User Management (Registration/Login with email and social auth)
- Admin Dashboard
- Real-time Tour Booking System
- Vendor Portal
- Payment Integration (Stripe)
- Real-time Updates (WebSocket)
- Blog/Content Management
- Google Maps Integration
- Review & Rating System

## Tech Stack

- Backend: Django
- Database: PostgreSQL
- Real-time: Django Channels + WebSocket
- Frontend: Bootstrap + HTMX
- Authentication: Django Allauth
- Payment Processing: Stripe
- Maps: Google Maps API

## Setup Instructions

1. Clone the repository
```bash
git clone <repository-url>
cd tours_travels
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create .env file in the project root and add the following variables:
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://user:password@localhost:5432/tours_travels
STRIPE_PUBLIC_KEY=your-stripe-public-key
STRIPE_SECRET_KEY=your-stripe-secret-key
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
```

5. Run migrations
```bash
python manage.py migrate
```

6. Create superuser
```bash
python manage.py createsuperuser
```

7. Run the development server
```bash
python manage.py runserver
```

Visit http://localhost:8000/admin to access the admin interface.

## Project Structure

- `core/` - Core functionality and shared components
- `accounts/` - User authentication and profile management
- `bookings/` - Tour booking and payment processing
- `vendors/` - Vendor portal and tour package management
- `blog/` - Blog and content management

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request #   d j a n g o - p r o j e c t 
 
 
