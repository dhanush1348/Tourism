#!/usr/bin/env python
"""Test Gemini API directly"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tours_project.settings')
django.setup()

from django.conf import settings
import google.generativeai as genai

try:
    print(f"API Key (first 20 chars): {settings.GOOGLE_API_KEY[:20]}...")
    genai.configure(api_key=settings.GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content('Tell me one fun fact about travel')
    print(f"Success! Response:\n{response.text}")
except Exception as e:
    print(f"Error: {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()
