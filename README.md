# 🌍 Wanderlust - Travel & Tours Booking Platform

A professional, production-ready Django web application for discovering and booking amazing travel experiences worldwide.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Deployment](#deployment)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

### Core Features
- 🏨 **Browse Destinations** - Explore beautiful travel destinations around the world
- 📦 **Tour Packages** - Discover curated tour packages with pricing and details
- 🔍 **Advanced Search** - Search packages by title, description, and destination
- 📅 **Easy Booking** - Simple booking form with number of participants
- ⭐ **Reviews & Ratings** - User reviews and ratings for packages
- 👤 **User Accounts** - Register, login, and manage bookings
- 📊 **Booking Management** - View booking history and confirmation details

### Professional Features
- 🔒 **Security** - HTTPS, CSRF protection, XSS prevention, SQL injection protection
- 📱 **Responsive Design** - Mobile-friendly interface with Bootstrap 5
- 🚀 **Performance** - Redis caching, optimized database queries
- 📊 **Logging** - Comprehensive application logging and error tracking
- 🏥 **Health Checks** - Monitoring endpoint for load balancers
- 🗺️ **SEO Optimized** - Sitemap, robots.txt, meta tags, Open Graph
- 📦 **PWA Ready** - Progressive Web App manifest for app-like experience

---

## 🛠️ Tech Stack

### Backend
- **Framework**: Django 5.2
- **Database**: PostgreSQL (production), SQLite (development)
- **Web Server**: Gunicorn + Nginx
- **Caching**: Redis
- **Task Queue**: Celery (optional)

### Frontend
- **Framework**: Bootstrap 5
- **Icons**: Font Awesome 6
- **Fonts**: Google Fonts (Inter)
- **Responsiveness**: Mobile-first design

### DevOps
- **Containerization**: Docker & Docker Compose
- **Version Control**: Git
- **Testing**: Pytest, Django TestCase
- **Code Quality**: Black, Flake8, Pylint

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 12+ (production)
- Redis (optional, for caching)
- Docker & Docker Compose (optional)

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/tours_project.git
cd tours_project
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
cp .env.example .env
# Edit .env with your settings
```

### 5. Setup Database
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### 6. Access Application
- **Home**: http://localhost:8000
- **Admin**: http://localhost:8000/admin
- **Health Check**: http://localhost:8000/health/

---

## 🐳 Docker Deployment

### Using Docker Compose
```bash
# Start all services
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Access at http://localhost
```

### Using Docker Alone
```bash
# Build image
docker build -t tours:latest .

# Run container
docker run -p 8000:8000 \
  -e ENVIRONMENT=development \
  -e DEBUG=True \
  tours:latest
```

---

## 📁 Project Structure

```
tours_project/
├── travel/                      # Main Django app
│   ├── models.py               # Database models
│   ├── views.py                # View logic (professional)
│   ├── views_seo.py            # SEO views (sitemap, health check)
│   ├── forms.py                # Form definitions
│   ├── tests.py                # 40+ comprehensive tests
│   ├── urls.py                 # URL routing
│   ├── admin.py                # Admin interface
│   ├── static/                 # Static files (CSS, JS, images)
│   │   └── travel/
│   │       ├── css/style.css
│   │       ├── manifest.json
│   │       └── images/
│   └── templates/              # HTML templates
│       └── travel/
│           ├── base.html       # Base template (SEO optimized)
│           ├── home.html
│           ├── package_list.html
│           ... (other templates)
│
├── tours_project/              # Project settings
│   ├── settings.py             # Settings (dev/prod)
│   ├── urls.py                 # Main URL config
│   ├── wsgi.py                 # WSGI entry point
│   └── asgi.py                 # ASGI entry point
│
├── Dockerfile                  # Docker image definition
├── docker-compose.yml          # Docker Compose orchestration
├── nginx.conf                  # Nginx reverse proxy config
├── requirements.txt            # Python dependencies
├── .env.example                # Environment template
├── .gitignore                  # Git ignore rules
├── manage.py                   # Django management script
├── DEPLOYMENT_GUIDE.md         # Detailed deployment guide
├── LAUNCH_CHECKLIST.md         # Pre-launch checklist
└── README.md                   # This file
```

---

## 🧪 Testing

### Run All Tests
```bash
# Using Django test runner
python manage.py test -v 2

# Using Pytest with coverage
pytest --cov=travel --cov-report=html
```

### Test Coverage
- **Model Tests**: Database validation (24 tests)
- **View Tests**: HTTP request/response (18 tests)
- **Form Tests**: Form validation (6 tests)
- **Total**: 40+ tests with 80%+ coverage

### Run Specific Tests
```bash
# Test a specific model
python manage.py test travel.tests.DestinationModelTest

# Test a specific view
python manage.py test travel.tests.PackageDetailViewTest

# Test with verbose output
python manage.py test travel -v 2
```

---

## 🚀 Deployment

### Quick Start Options

#### Heroku
```bash
heroku create tours-wanderlust
heroku config:set ENVIRONMENT=production SECRET_KEY=<key>
heroku addons:create heroku-postgresql
heroku addons:create heroku-redis
git push heroku main
```

#### AWS (ECS + RDS + ElastiCache)
See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed AWS setup.

#### DigitalOcean
```bash
doctl apps create --spec app.yaml
```

#### VPS with Docker
See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for VPS setup.

### Production Checklist
- [ ] `DEBUG = False`
- [ ] `SECRET_KEY` is random and secure
- [ ] `ALLOWED_HOSTS` configured
- [ ] SSL certificate installed
- [ ] Database backup configured
- [ ] Email service configured
- [ ] Logging and monitoring set up
- [ ] All tests passing

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for complete deployment instructions.

---

## 📚 Documentation

### Available Documentation
1. **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Complete deployment guide
   - Environment setup
   - Testing procedures
   - Deployment options (Heroku, AWS, DigitalOcean, VPS)
   - Post-deployment verification
   - Monitoring and maintenance

2. **[LAUNCH_CHECKLIST.md](LAUNCH_CHECKLIST.md)** - Pre-launch requirements
   - Code quality requirements
   - SEO optimization
   - Security checklist
   - Performance metrics
   - Legal compliance items

### Code Documentation
All functions include docstrings with:
- Function purpose
- Arguments and return values
- Type hints for better IDE support
- Examples where applicable

---

## 🔒 Security Features

✅ **Implemented**
- HTTPS/SSL enforced in production
- CSRF token protection
- XSS prevention via template escaping
- SQL injection protection (Django ORM)
- Secure password hashing
- Security headers (HSTS, X-Frame-Options, etc.)
- Input validation on all forms
- Admin panel authentication
- Environment variable secrets management

---

## 📊 API Endpoints

### Public Endpoints
```
GET  /                          # Home page
GET  /destinations/             # Destination list (paginated)
GET  /destinations/<id>/        # Destination detail
GET  /packages/                 # Package list (filtered, paginated)
GET  /packages/<id>/            # Package detail with forms
POST /packages/<id>/            # Submit booking/review
GET  /search/                   # Search packages
GET  /login/                    # Login form
POST /login/                    # Submit login
GET  /register/                 # Register form
POST /register/                 # Submit registration
```

### Health & SEO Endpoints
```
GET  /health/                   # Health check (JSON)
GET  /sitemap.xml               # XML sitemap
GET  /robots.txt                # Robots.txt
```

---

## 🔧 Configuration

### Environment Variables
```bash
# Django
ENVIRONMENT=production          # development or production
DEBUG=False                      # Always False in production
SECRET_KEY=<generated-key>       # Run: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
ALLOWED_HOSTS=yourdomain.com

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=tours_db
DB_USER=postgres
DB_PASSWORD=<secure-password>
DB_HOST=localhost
DB_PORT=5432

# Cache
REDIS_URL=redis://localhost:6379/1

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=app-password

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests for new features
4. Ensure all tests pass (`pytest`)
5. Commit changes (`git commit -m 'Add amazing feature'`)
6. Push to branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Code Standards
- Run `black` for code formatting
- Run `flake8` for linting
- Maintain > 80% test coverage
- Add docstrings to all functions
- Use type hints

---

## 📈 Performance Metrics

Target metrics for production:

| Metric | Target | How to Achieve |
|--------|--------|---|
| Page Load Time | < 2 seconds | CDN, caching, image optimization |
| Uptime | > 99.5% | Monitoring, redundancy, backups |
| Error Rate | < 0.1% | Testing, logging, error tracking |
| Response Time | < 200ms | Database optimization, caching |
| Lighthouse Score | > 85 | Optimization, minification, lazy loading |

---

## 🆘 Troubleshooting

### Common Issues

**Issue**: Database connection error
```bash
# Solution: Check database service
sudo systemctl status postgresql
python manage.py migrate
```

**Issue**: Static files not loading
```bash
# Solution: Collect static files
python manage.py collectstatic --noinput
```

**Issue**: 500 errors in production
```bash
# Solution: Check logs
docker-compose logs web
heroku logs --tail
```

See full troubleshooting guide in [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md).

---

## 📞 Support

- **Documentation**: See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **Issues**: Open an issue on GitHub
- **Email**: support@wanderlust.com

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 👏 Acknowledgments

- Django community for the amazing framework
- Bootstrap for responsive design
- All contributors and testers

---

## 🎉 Version History

### v1.0.0 (2025-03-30)
✨ Initial production release
- Professional code refactoring with type hints
- 40+ comprehensive unit tests
- Production-ready configuration
- Docker containerization
- SEO optimization
- Security hardening
- Complete deployment guide

---

**Last Updated**: March 30, 2026  
**Status**: ✅ Production Ready  
**Maintainer**: Wanderlust Team
