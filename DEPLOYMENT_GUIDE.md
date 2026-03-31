# 🚀 Wanderlust Tours - Production Deployment Guide

## Pre-Deployment Checklist

### ✅ Code & Security
- [x] Code professionally refactored with type hints and docstrings
- [x] Comprehensive test suite created (40+ tests)
- [x] Environment-based configuration (dev/production)
- [x] Security headers configured
- [x] HTTPS/SSL enforced in production
- [x] CSRF and XSS protection enabled

### ✅ Database
- [x] Models designed with proper relationships
- [x] Migrations ready for deployment
- [x] PostgreSQL support configured
- [x] Database backups strategy

### ✅ SEO & Metadata
- [x] Meta tags and Open Graph tags implemented
- [x] Sitemap.xml generated dynamically
- [x] robots.txt configured
- [x] Favicon and app icons support
- [x] Canonical URLs set
- [x] Mobile responsive design
- [x] PWA manifest.json created

### ✅ Monitoring & Logging
- [x] Health check endpoint (/health/)
- [x] Structured logging configured
- [x] Log rotation enabled
- [x] Error tracking ready for Sentry

### ✅ Performance
- [x] Static file optimization
- [x] Redis caching configured
- [x] Database connection pooling
- [x] Nginx reverse proxy ready

### ✅ Deployment Infrastructure
- [x] Docker containerization
- [x] Docker Compose for local testing
- [x] Gunicorn WSGI server configured
- [x] Environment variables support

---

## Environment Setup

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd tours_project
```

### 2. Create Environment File
```bash
cp .env.example .env
```

### 3. Configure .env for Production
```bash
# Critical: Generate a new SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Update .env with production values
ENVIRONMENT=production
SECRET_KEY=<generated-secret-key>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_NAME=tours_db
DB_USER=postgres
DB_PASSWORD=<secure-password>
DB_HOST=<db-host>
DB_PORT=5432

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=<your-email>
EMAIL_HOST_PASSWORD=<app-password>

# Redis
REDIS_URL=redis://<redis-host>:6379/1

# Admin
ADMINS=Admin Name|admin@example.com
```

---

## Local Development Testing

### 1. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Tests
```bash
# Run all tests
python manage.py test

# Run with coverage report
pytest --cov=travel tests.py

# Run specific test
python manage.py test travel.tests.DestinationModelTest
```

### 4. Run Development Server
```bash
python manage.py migrate
python manage.py runserver
```

### 5. Docker Testing
```bash
# Build and run with Docker Compose
docker-compose up -d

# Check logs
docker-compose logs -f web

# Run migrations in container
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

---

## Running Tests

### Test Coverage Report
```bash
# Run tests with coverage
pytest --cov=travel --cov-report=html

# View coverage in browser
open htmlcov/index.html
```

### Test Categories
- **Model Tests**: Database model validation (24 tests)
- **View Tests**: HTTP request/response handling (18 tests)
- **Form Tests**: Form validation (6 tests)
- **Integration Tests**: End-to-end scenarios

### Key Tests
```bash
# Test destination management
python manage.py test travel.tests.DestinationModelTest

# Test package booking flow
python manage.py test travel.tests.PackageDetailViewTest

# Test user authentication
python manage.py test travel.tests.LoginViewTest.test_login_successful
```

---

## Production Deployment Options

### Option 1: Heroku Deployment

#### 1. Create Heroku App
```bash
heroku create tours-wanderlust
```

#### 2. Add Add-ons
```bash
heroku addons:create heroku-postgresql:standard-0
heroku addons:create heroku-redis:premium-0
```

#### 3. Configure Environment
```bash
heroku config:set ENVIRONMENT=production
heroku config:set SECRET_KEY=<generated-key>
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=tours-wanderlust.herokuapp.com
```

#### 4. Create Procfile
```
web: gunicorn tours_project.wsgi:application
release: python manage.py migrate
```

#### 5. Deploy
```bash
git push heroku main
```

### Option 2: AWS Deployment (ECS + RDS + ElastiCache)

#### 1. RDS Setup
```bash
# Create PostgreSQL database
aws rds create-db-instance \
  --db-instance-identifier tours-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --allocated-storage 20
```

#### 2. ElastiCache Setup
```bash
# Create Redis cluster
aws elasticache create-cache-cluster \
  --cache-cluster-id tours-redis \
  --engine redis \
  --cache-node-type cache.t3.micro
```

#### 3. ECR & ECS
```bash
# Create ECR repository
aws ecr create-repository --repository-name tours

# Build and push Docker image
docker build -t tours:latest .
docker tag tours:latest <account-id>.dkr.ecr.<region>.amazonaws.com/tours:latest
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/tours:latest
```

### Option 3: DigitalOcean App Platform

#### 1. Create app.yaml
```yaml
name: wanderlust
services:
- name: web
  github:
    repo: <your-repo>
    branch: main
  build_command: pip install -r requirements.txt && python manage.py collectstatic --noinput
  run_command: gunicorn tours_project.wsgi:application
  http_port: 8000
  envs:
  - key: ENVIRONMENT
    value: production
  - key: DEBUG
    value: "False"

databases:
- name: tours-db
  engine: PG
  version: "12"

- name: tours-redis
  engine: REDIS
  version: "6"
```

#### 2. Deploy
```bash
doctl apps create --spec app.yaml
```

### Option 4: Docker with Nginx on VPS

#### 1. Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker & Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Start services
sudo systemctl start docker
sudo systemctl enable docker
```

#### 2. Deploy Application
```bash
# Clone repository
git clone <your-repo>
cd tours_project

# Copy .env for production
cp .env.example .env
# Edit .env with production values

# Start services
sudo docker-compose -f docker-compose.yml up -d

# Run migrations
sudo docker-compose exec web python manage.py migrate

# Collect static files
sudo docker-compose exec web python manage.py collectstatic --noinput

# Create superuser
sudo docker-compose exec web python manage.py createsuperuser
```

#### 3. Configure SSL with Let's Encrypt
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Generate certificate
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Update nginx.conf with SSL
sudo certbot install --nginx
```

---

## Post-Deployment Verification

### 1. Health Checks
```bash
# Check application health
curl https://yourdomain.com/health/
# Expected: {"status": "healthy", ...}

# Check sitemap
curl https://yourdomain.com/sitemap.xml
# Expected: Valid XML sitemap

# Check robots.txt
curl https://yourdomain.com/robots.txt
# Expected: Valid robots.txt
```

### 2. Security Checks
```bash
# Check SSL certificate
curl -I https://yourdomain.com
# Verify HSTS headers present

# Check security headers
curl -I https://yourdomain.com | grep -i "strict-transport-security"

# Test HTTPS redirect
curl -I http://yourdomain.com
# Expected: 301 redirect to https
```

### 3. SEO Verification
```bash
# Google Search Console
# 1. Add property for yourdomain.com
# 2. Submit sitemap.xml
# 3. Test robots.txt
# 4. Check URL inspection
```

### 4. Performance Checks
```bash
# Test with PageSpeed Insights
# https://pagespeed.web.dev/

# Monitor with Sentry
# 1. Create Sentry project
# 2. Add SENTRY_DSN to .env
# 3. Test error tracking
```

---

## Monitoring & Maintenance

### 1. Application Logs
```bash
# For Docker:
docker-compose logs -f web

# For Heroku:
heroku logs --tail

# For AWS:
aws logs tail /ecs/tours --follow
```

### 2. Database Backups
```bash
# PostgreSQL backup
pg_dump tours_db > backup-$(date +%Y%m%d).sql

# Automated backups (daily)
0 2 * * * pg_dump tours_db > /backups/backup-$(date +\%Y\%m\%d).sql
```

### 3. Monitor Metrics
- Application uptime
- Response time (target: < 200ms)
- Error rate (target: < 0.1%)
- Database connections
- Cache hit rate

### 4. Regular Maintenance
```bash
# Update dependencies (monthly)
pip install --upgrade -r requirements.txt

# Database cleanup (weekly)
python manage.py cleanupexpiredtokens

# Static file optimization (after changes)
python manage.py collectstatic --noinput
```

---

## Scaling Recommendations

### Horizontal Scaling
1. **Load Balancer**: Nginx, HAProxy, or AWS ELB
2. **Multiple App Servers**: Run multiple Gunicorn workers
3. **Database Replication**: PostgreSQL master-slave setup
4. **CDN**: CloudFront or Cloudflare for static assets

### Vertical Scaling
1. Increase server resources (CPU, RAM)
2. Optimize database queries
3. Implement caching strategies
4. Optimize images and assets

### Caching Strategy
```python
# Page caching (5 minutes)
@cache_page(60 * 5)
def expensive_view(request):
    pass

# Query result caching
destinations = cache.get_or_set('all_destinations', 
    lambda: list(Destination.objects.all()), 
    60 * 60  # 1 hour
)
```

---

## Troubleshooting

### Common Issues

#### 1. Database Connection Errors
```bash
# Check PostgreSQL service
sudo systemctl status postgresql

# Check connection string
python manage.py shell
from django.db import connection
connection.ensure_connection()
```

#### 2. Static Files Not Loading
```bash
# Collect static files
python manage.py collectstatic --noinput

# Check static file directory
ls -la staticfiles/

# Verify nginx configuration
sudo nginx -t
```

#### 3. Memory Issues
```bash
# Check memory usage
free -h
docker stats

# Optimize Gunicorn workers
# workers = 2 + (2 × CPU cores)
```

#### 4. Slow Queries
```bash
# Enable query logging
LOGGING['loggers']['django.db.backends']['level'] = 'DEBUG'

# Use Django Debug Toolbar (development only)
# pip install django-debug-toolbar
```

---

## Security Checklist

- [ ] SECRET_KEY is truly random and kept secret
- [ ] DEBUG = False in production
- [ ] ALLOWED_HOSTS configured correctly
- [ ] HTTPS/SSL enabled and enforced
- [ ] CSRF tokens enabled
- [ ] SQL injection protection (Django ORM)
- [ ] XSS protection enabled
- [ ] CORS headers configured
- [ ] Rate limiting implemented
- [ ] Input validation on all forms
- [ ] Secure password hashing
- [ ] Admin panel protected
- [ ] Database backups tested
- [ ] Regular security updates

---

## Contact & Support

- **Admin**: admin@wanderlust.com
- **Support**:support@wanderlust.com
- **Documentation**: https://docs.wanderlust.com
- **Status Page**: https://status.wanderlust.com

---

## Version History

- **v1.0.0** (2025-03-30): Initial production release
  - Professional code refactoring
  - Comprehensive test suite
  - Production-ready configuration
  - Docker containerization
  - SEO optimization
  - Security hardening
