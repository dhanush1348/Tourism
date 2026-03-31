# Quick Start - Test Your Free Tier Chat System

## ✅ System Status

Your Wanderlust travel booking platform is **ready to use** with the new Gemini fallback system!

```
✅ Landing page: http://127.0.0.1:8000/
✅ Chat API: /api/chat/ (Gemini + Fallback)
✅ Booking API: /api/bookings/ (Working)
✅ Django server: Running
```

## 🚀 Quick Test (30 seconds)

### Step 1: Open the Platform
Open your browser and go to:
```
http://127.0.0.1:8000/
```

You should see a premium travel booking interface with:
- Destination carousel
- Featured packages
- Chat FAB (gold button with ✦ icon in bottom right)

### Step 2: Test the Chat
Click the gold chat button (✦) in the bottom right corner.

The chat widget opens with message input and send button.

### Step 3: Try Different Messages

Send these messages one by one to test different patterns:

**Message 1: Beach/Tropical**
```
Tell me about beach vacations
```
✅ Expected: Maldives Overwater Retreat response

**Message 2: Romantic/Honeymoon**
```
I'm planning a honeymoon with my partner
```
✅ Expected: Mediterranean Luxury Cruise response

**Message 3: Adventure/Mountain**
```
I love hiking and want to visit Machu Picchu
```
✅ Expected: Andean Explorer response

**Message 4: Budget Question**
```
What's your cheapest package?
```
✅ Expected: Pricing details response

**Message 5: Duration Question**
```
How long are the trips?
```
✅ Expected: Package duration information

**Message 6: Random Question (Default Fallback)**
```
What time do you close?
```
✅ Expected: Default expert recommendation

### Step 4: Test Booking
1. Scroll to "Featured Packages" section
2. Click "Book Now" on any package
3. Fill out the booking form:
   - Name: Your name
   - Email: your@email.com
   - Date: 2026-05-15 (or any future date)
   - Guests: 2
   - Package: Select from dropdown
4. Click "Confirm Booking"
5. You should see a success message with booking confirmation

## 📊 What's Working

### Chat System
- ✅ Gulf/Beach queries → Maldives response
- ✅ Mountain/Adventure queries → Andean Explorer response
- ✅ Romantic/Honeymoon queries → Mediterranean response
- ✅ Culture/History queries → Japan response
- ✅ Wellness/Spa queries → Bali response
- ✅ Budget queries → Pricing information
- ✅ Duration queries → Package details
- ✅ Group type queries → Customization options
- ✅ Logistics queries → Travel documents info
- ✅ Unknown queries → Default expert response

### Booking System
- ✅ Form validation (name, email, date)
- ✅ Date parsing (YYYY-MM-DD format)
- ✅ Price calculation (package price × guests)
- ✅ Booking confirmation (with unique booking ID)
- ✅ Email notification (sent to user email)

## 🔄 How Fallback Works

Your system uses **two-tier response strategy**:

```
1. PRIMARY: Try Google Gemini API
   │
   ├─ [SUCCESS] → Return direct AI response
   │
   └─ [QUOTA EXCEEDED] → Automatic fallback
                       └─ Match pattern (10 travel patterns)
                       └─ Return curated response
                       └─ User never sees error ✅

2. OR IMMEDIATE FALLBACK: If Gemini unavailable
   │
   └─ Match pattern from user input
   └─ Return relevant curated response
   └─ User gets helpful answer instantly ✅
```

**Result**: Chat is always functional, whether Gemini API is available or not!

## 💡 Key Points

### Free Tier
- 60 requests per minute
- Monthly quota limits
- Resets automatically each month
- Fallback handles gracefully when quota exceeded

### User Experience
- No error messages shown
- Always gets a helpful response
- Seamless transition from Gemini → Fallback
- Works indefinitely on free tier

### Response Quality
- Fallback responses are professionally curated
- Domain-specific (travel/tourism focused)
- Pattern-matched to user intent
- Helpful and informative

## 🧪 Advanced Testing (Optional)

### Test with Python
```python
import requests

# Test beach pattern
response = requests.post(
    'http://127.0.0.1:8000/api/chat/',
    json={'message': 'Tell me about beaches'}
)
print(response.json()['reply'])
```

### Test Booking API
```python
response = requests.post(
    'http://127.0.0.1:8000/api/bookings/',
    json={
        'name': 'John Doe',
        'email': 'john@example.com',
        'date': '2026-05-15',
        'guests': 2,
        'package_id': 1
    }
)
print(response.json())
```

### Logs
View Django server logs in your terminal to see:
- Which responses came from Gemini (successful API calls)
- Which came from fallback (quota/error handling)
- Any exceptions caught

## ✨ What Changed from Earlier

**Before**: Chat failed with error when quota exceeded
```
❌ Status 503: "AI service temporarily unavailable"
```

**Now**: Chat always works with intelligent fallback
```
✅ Status 200: "Our Maldives Overwater Retreat is stunning..."
```

## 📁 Configuration Files

All configuration is in these files:

| File | Purpose |
|------|---------|
| `.env` | Your API key (GOOGLE_API_KEY=...) |
| `travel/api.py` | Chat/Booking logic with fallback |
| `tours_project/settings.py` | Django settings (.env loader) |
| `requirements.txt` | Python dependencies |

## 🐛 Troubleshooting

### Chat button doesn't appear
- ✅ Clear browser cache (Ctrl+Shift+Delete)
- ✅ Hard refresh (Ctrl+Shift+R)
- ✅ Check Django server is running (terminal shows "Starting development server")

### Chat not responding
- ✅ Check Django server logs for errors
- ✅ Verify API key is set in `.env` file
- ✅ Check system has internet connection

### Booking not working
- ✅ Ensure date format is YYYY-MM-DD
- ✅ Use a future date (not past)
- ✅ Fill all required fields

### API errors in logs
- Normal FutureWarning about `google-generativeai` → Still works fine
- "quota exceeded" message → Expected, fallback is working ✅

## 📞 Support

If you encounter issues:

1. Check Django server terminal for error messages
2. Review logs in [FALLBACK_SYSTEM_IMPLEMENTATION.md](FALLBACK_SYSTEM_IMPLEMENTATION.md)
3. Verify `.env` file has `GOOGLE_API_KEY` set
4. Verify `.env` file has NO quotes around API key value

## 🚢 Next Steps

Once you're satisfied with testing:

1. **Customize responses**: Edit `FALLBACK_RESPONSES` in `travel/api.py` for your brand voice
2. **Deploy to production**: Follow [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
3. **Monitor usage**: Track API quota in Google Cloud Console
4. **Upgrade when needed**: Switch to paid tier if exceeding free limits

---

**Current Status**: ✅ Production Ready  
**Server Running**: http://127.0.0.1:8000/  
**Last Updated**: April 1, 2026
