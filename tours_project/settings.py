"""
Django settings for tours_project project.

This settings module supports both development and production environments.
Configuration is controlled via environment variables.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# Load environment variables from .env file
load_dotenv(Path(__file__).resolve().parent.parent / '.env')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================================================
# ENVIRONMENT CONFIGURATION
# ============================================================================

# Get environment (development or production)
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development').lower()
IS_PRODUCTION = ENVIRONMENT == 'production'

# Security: load SECRET_KEY from environment
SECRET_KEY = os.getenv(
    'SECRET_KEY',
    'django-insecure-&@x4$)wts+3f3xvn#%!qd*#0d5yha_=beyfc#4v3csk6-&0!yq'
    if not IS_PRODUCTION
    else None
)

if not SECRET_KEY and IS_PRODUCTION:
    raise ValueError("SECRET_KEY environment variable is required in production")

# Debug mode - never True in production
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 'on')
if IS_PRODUCTION:
    DEBUG = False

# Allowed hosts from environment
default_hosts = 'localhost,127.0.0.1,.pythonanywhere.com' if IS_PRODUCTION else 'localhost,127.0.0.1'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', default_hosts).split(',')
ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS]

# CSRF trusted origins for HTTPS deployments behind reverse proxy (e.g. PythonAnywhere)
default_csrf_origins = 'https://*.pythonanywhere.com' if IS_PRODUCTION else ''
CSRF_TRUSTED_ORIGINS = [
    origin.strip() for origin in os.getenv('CSRF_TRUSTED_ORIGINS', default_csrf_origins).split(',')
    if origin.strip()
]

# Google Gemini API Key for chatbot
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', 'your-key-here')

# ============================================================================
# APPLICATION DEFINITION
# ============================================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'travel',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tours_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'tours_project.wsgi.application'

# ============================================================================
# DATABASE
# ============================================================================

# Support both SQLite (development) and PostgreSQL (production)
if IS_PRODUCTION:
    database_url = os.getenv('DATABASE_URL', '').strip()
    if database_url:
        DATABASES = {
            'default': dj_database_url.parse(database_url, conn_max_age=600)
        }
        DATABASES['default']['ATOMIC_REQUESTS'] = True
    else:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ============================================================================
# PASSWORD VALIDATION
# ============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ============================================================================
# INTERNATIONALIZATION
# ============================================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ============================================================================
# STATIC & MEDIA FILES
# ============================================================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'travel' / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ============================================================================
# DEFAULT PRIMARY KEY FIELD
# ============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================================================
# SECURITY SETTINGS (Production)
# ============================================================================

if IS_PRODUCTION:
    # HTTPS
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    USE_X_FORWARDED_HOST = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # HSTS (HTTP Strict Transport Security)
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Other security settings
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
    SECURE_CONTENT_SECURITY_POLICY = {
        'default-src': ("'self'",),
        'script-src': ("'self'", "'unsafe-inline'"),
        'style-src': ("'self'", "'unsafe-inline'"),
        'img-src': ("'self'", "data:", "https:"),
    }
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_PRELOAD = True

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'maxBytes': 1024 * 1024 * 5,  # 5MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'travel': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
    },
}

# Create logs directory if it doesn't exist
os.makedirs(BASE_DIR / 'logs', exist_ok=True)

# ============================================================================
# EMAIL CONFIGURATION
# ============================================================================

EMAIL_BACKEND = os.getenv(
    'EMAIL_BACKEND',
    'django.core.mail.backends.console.EmailBackend'
    if not IS_PRODUCTION
    else 'django.core.mail.backends.smtp.EmailBackend'
)

if IS_PRODUCTION:
    EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
    EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() in ('true', '1', 'on')
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
    DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@tours.com')

# ============================================================================
# CACHE CONFIGURATION
# ============================================================================

if IS_PRODUCTION:
    redis_url = os.getenv('REDIS_URL', '').strip()
    if redis_url:
        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.redis.RedisCache',
                'LOCATION': redis_url,
                'TIMEOUT': 300,
            }
        }
    else:
        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                'LOCATION': 'tours-cache-prod',
            }
        }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'tours-cache',
        }
    }

# ============================================================================
# SESSION & COOKIE SETTINGS
# ============================================================================

SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# ============================================================================
# ADMIN SETTINGS
# ============================================================================

ADMINS = [
    (name, email.strip())
    for name, email in (
        pair.split('|') for pair in os.getenv('ADMINS', '').split(';')
        if pair and '|' in pair
    )
]

