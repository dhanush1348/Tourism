"""
API endpoints for Wanderlust chatbot and booking system.
"""

import json
import logging
import re
from datetime import datetime
from typing import Any, Dict

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from django.conf import settings

import google.generativeai as genai

logger = logging.getLogger(__name__)

# Initialize Google Gemini client
try:
    if settings.GOOGLE_API_KEY and settings.GOOGLE_API_KEY != 'your-key-here':
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        GEMINI_AVAILABLE = True
    else:
        GEMINI_AVAILABLE = False
except Exception as e:
    logger.warning(f"Gemini client init warning: {str(e)}")
    GEMINI_AVAILABLE = False

SYSTEM_PROMPT = """You are Aria, the luxury travel concierge for Wanderlust — a premium travel & tours platform. 
Help users discover destinations, plan itineraries, find the perfect tour package, and book experiences. 
Be warm, sophisticated, and knowledgeable. Keep responses concise (2-3 sentences max unless asked for detail). 
Always end with a follow-up question or suggestion.

Available packages:
- Greek Islands Odyssey ($2,490/10 days)
- Japan Cherry Blossom Trail ($3,850/14 days)
- Andean Explorer ($2,990/12 days)
- Mediterranean Luxury Cruise ($4,200/8 days)
- Bali Spirit Journey ($1,890/9 days)
- Maldives Overwater Retreat ($5,600/7 days)"""

# Fallback responses for free tier (curated by travel experts)
FALLBACK_RESPONSES = {
    # Destination inquiries
    r'(beach|maldives|tropical|island)': "Our Maldives Overwater Retreat is absolutely stunning—pristine turquoise waters, luxury overwater bungalows, and world-class diving. Perfect for beach lovers seeking ultimate paradise. Would you like details on snorkeling packages or sunset experiences?",
    
    r'(mountain|hiking|adventure|trek|machu picchu|peru)': "The Andean Explorer is ideal for adventure seekers! You'll experience breathtaking mountain vistas, ancient Incan heritage, and immersive local culture. Our guides ensure both comfort and authentic experiences. Interested in altitude acclimatization tips or cultural experiences?",
    
    r'(culture|history|temple|kyoto|japan)': "Japan's Cherry Blossom Trail combines ancient temples, serene gardens, and rich cultural heritage. You'll experience tea ceremonies, traditional kaiseki dinners, and the magic of cherry blossoms in spring. Which aspects of Japanese culture fascinate you most?",
    
    r'(romantic|honeymoon|couple|anniversary)': "The Mediterranean Luxury Cruise is perfect for couples! Imagine sunset dinners in elegant settings, private cabin experiences, and romantic ports across Italy, Greece, and Croatia. Shall I details on romantic add-ons or cabin upgrades?",
    
    r'(wellness|spa|relax|yoga|bali)': "Bali Spirit Journey combines wellness retreats, yoga sessions, and spa treatments in a tropical paradise. You'll find inner peace at sacred temples, organic farms, and wellness resorts. What wellness experience appeals to you—yoga, meditation, or Ayurvedic spa treatments?",
    
    # Budget/Pricing  
    r'(price|cost|budget|afford|cheap|expensive)': "Our packages range from $1,890 (Bali Spirit Journey) to $5,600 (Maldives Retreat) per person. Each includes accommodation, activities, and curated experiences. Would you like a custom itinerary within your budget, or shall I suggest the best value-for-experience options?",
    
    # Duration/Timing
    r'(how long|days|duration|when|dates|months)': "Our packages range from 7-14 days. Most travelers find 10 days ideal for immersion without burnout. Peak seasons vary by destination—spring for Japan, winter for Caribbean. Which destination interests you, and what's your preferred timeframe?",
    
    # Group/Travelers
    r'(solo|alone|single|group|family|kids|children)': "We accommodate all group types! Solo travelers often join our group tours for connection. Families enjoy our customized itineraries. We can arrange private guides, kid-friendly activities, and family suites. How many travelers are in your group, and any special needs?",
    
    # General travel questions
    r'(visa|passport|documents|flights)': "We handle all travel logistics! Our team assists with visa guidance, flight arrangements, travel insurance, and pre-departure briefings. You focus on packing your dreams—we handle the details. Which destination are you leaning toward?",
    
    r'(when|soon|available|next|booking)': "We offer flexible booking! Most itineraries depart year-round with seasonal variations in cost. Spring and fall offer the best weather across destinations. Shall we discuss your dream timeframe and lock in your adventure?",
    
    r'(thanks|thank you|great|perfect|awesome)': "Delighted to help! Your adventure awaits. Ready to reserve your journey or have more questions about specific packages? Our team is here to craft the perfect experience for you! ✨",
}

def get_fallback_response(user_input: str) -> str:
    """
    Get a relevant fallback response based on user input keywords.
    Used when API quota is exceeded or unavailable.
    """
    user_lower = user_input.lower()
    
    # Try to match user input with fallback response patterns
    for pattern, response in FALLBACK_RESPONSES.items():
        if re.search(pattern, user_lower):
            return response
    
    # Default fallback if no pattern matches
    return f"That's a great question! At Wanderlust, we curate extraordinary journeys to destinations like Greece, Japan, Peru, Italy, Indonesia, and the Maldives. Each package combines luxury accommodations, authentic experiences, and expert guidance. Which destination speaks to your travel dreams?"


@csrf_exempt
@require_http_methods(["POST"])
def chat_view(request: dict) -> JsonResponse:
    """
    AI chatbot endpoint powered by Google Gemini with intelligent fallback.
    
    Expected POST data:
        {
            "message": "user message",
            "history": [{"role": "user"/"bot", "text": "..."}]
        }
    """
    try:
        data = json.loads(request.body)
        user_message = data.get("message", "").strip()
        history = data.get("history", [])

        if not user_message:
            return JsonResponse({"error": "Message cannot be empty"}, status=400)

        # Try to use Gemini API if available
        if GEMINI_AVAILABLE:
            try:
                # Build conversation history for Gemini
                prompt = f"{SYSTEM_PROMPT}\n\n"
                
                # Add conversation history
                for msg in history:
                    role = "User" if msg["role"] == "user" else "Aria"
                    prompt += f"{role}: {msg['text']}\n"
                
                # Add current user message
                prompt += f"User: {user_message}\nAria:"

                # Call Gemini API
                model = genai.GenerativeModel(model_name="gemini-2.0-flash")
                
                response = model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        max_output_tokens=500,
                        temperature=0.7
                    )
                )

                reply = response.text.strip()
                logger.info(f"Chat via Gemini: {user_message[:50]}...")
                return JsonResponse({"reply": reply})
            
            except Exception as api_error:
                api_error_str = str(api_error).lower()
                
                # If it's a quota error, use fallback
                if "quota" in api_error_str or "rate_limit" in api_error_str or "resource_exhausted" in api_error_str:
                    logger.info(f"Gemini quota exceeded, using fallback for: {user_message[:50]}...")
                    reply = get_fallback_response(user_message)
                    return JsonResponse({"reply": reply})
                
                # If it's an auth error, report it
                elif "api_key" in api_error_str or "authentication" in api_error_str:
                    logger.error(f"Gemini API key error: {str(api_error)}")
                    return JsonResponse(
                        {"error": "API configuration error. Please check your Google API key."},
                        status=503
                    )
                
                # Other errors, fall back to curated responses
                else:
                    logger.warning(f"Gemini API error, using fallback: {str(api_error)[:100]}")
                    reply = get_fallback_response(user_message)
                    return JsonResponse({"reply": reply})
        
        else:
            # Gemini not available, use fallback immediately
            logger.info(f"Gemini unavailable, using fallback for: {user_message[:50]}...")
            reply = get_fallback_response(user_message)
            return JsonResponse({"reply": reply})

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        logger.error(f"Chat endpoint error: {str(e)}")
        # Even if something goes wrong, provide a fallback response
        return JsonResponse(
            {"reply": "I encountered a brief hiccup, but I'm here to help! Tell me about your dream destination, and I'll suggest the perfect Wanderlust package for you. ✈️"},
            status=200
        )


@csrf_exempt
@require_http_methods(["POST"])
def booking_view(request: dict) -> JsonResponse:
    """
    Create a new booking.
    
    Expected POST data:
        {
            "name": "John Doe",
            "email": "john@example.com",
            "date": "2026-05-15",
            "guests": "2",
            "package_id": 1
        }
    """
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required = ["name", "email", "date", "guests", "package_id"]
        if not all(field in data for field in required):
            return JsonResponse(
                {"error": "Missing required fields"},
                status=400
            )

        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        travel_date = data.get("date", "").strip()
        guests = int(data.get("guests", 1))
        package_id = int(data.get("package_id", 1))

        # Basic validation
        if not name or not email:
            return JsonResponse(
                {"error": "Name and email are required"},
                status=400
            )

        # Parse date
        try:
            travel_date_obj = datetime.strptime(travel_date, "%Y-%m-%d").date()
        except ValueError:
            return JsonResponse(
                {"error": "Invalid date format. Use YYYY-MM-DD"},
                status=400
            )

        # Package details (would normally come from database)
        packages = {
            1: {"name": "Greek Islands Odyssey", "price": 2490},
            2: {"name": "Japan Cherry Blossom Trail", "price": 3850},
            3: {"name": "Andean Explorer", "price": 2990},
            4: {"name": "Mediterranean Luxury Cruise", "price": 4200},
            5: {"name": "Bali Spirit Journey", "price": 1890},
            6: {"name": "Maldives Overwater Retreat", "price": 5600},
        }

        if package_id not in packages:
            return JsonResponse(
                {"error": "Invalid package ID"},
                status=400
            )

        pkg = packages[package_id]
        total_price = pkg["price"] * guests

        # Log booking
        booking_info = {
            "name": name,
            "email": email,
            "package": pkg["name"],
            "date": travel_date,
            "guests": guests,
            "total": total_price,
            "timestamp": datetime.now().isoformat()
        }
        logger.info(f"Booking created: {json.dumps(booking_info)}")

        # Send confirmation email
        try:
            send_mail(
                subject=f"Wanderlust Booking Confirmation - {pkg['name']}",
                message=f"""
Dear {name},

Thank you for booking with Wanderlust!

Package: {pkg['name']}
Travel Date: {travel_date}
Number of Guests: {guests}
Total Price: ${total_price:,}

Your adventure awaits! We'll be in touch with more details soon.

Best regards,
Aria & The Wanderlust Team
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=True
            )
        except Exception as e:
            logger.error(f"Email sending error: {str(e)}")

        return JsonResponse({
            "success": True,
            "booking_id": f"WL-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "message": f"Booking confirmed! Confirmation sent to {email}",
            "total": total_price
        })

    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        return JsonResponse({"error": "Invalid input data"}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        logger.error(f"Booking error: {str(e)}")
        return JsonResponse({"error": "An error occurred creating your booking."}, status=500)


@require_http_methods(["GET"])
def landing_view(request):
    """Render the premium landing page with React."""
    from django.shortcuts import render
    return render(request, "travel/landing.html")
