"""
WSGI config for tours_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from django.core.wsgi import get_wsgi_application

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
	sys.path.insert(0, str(BASE_DIR))

# Ensure environment variables from .env are available for all WSGI hosts.
load_dotenv(BASE_DIR / '.env')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tours_project.settings')

application = get_wsgi_application()
