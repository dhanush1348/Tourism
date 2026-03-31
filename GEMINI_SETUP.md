# ✨ Google Gemini API Setup Guide

## 🚀 Quick Setup (5 minutes)

Your premium landing page with Aria (AI chatbot) powered by Google Gemini is ready! Follow these steps to activate the chat functionality.

### Step 1: Get Your Google API Key

1. **Open Google AI Studio**
   - Go to: https://aistudio.google.com/app/apikey
   - You may need to sign in with your Google account
   
2. **Create API Key**
   - Click the **"Create API Key"** button
   - Select **"Create API Key in new project"** or use an existing project
   - Copy the API key (it's a long string)

3. **Enable Gemini API** (if needed)
   - The API should be automatically enabled
   - If error occurs, ensure you're using a valid Google account

### Step 2: Add Key to .env File

1. Open `.env` file in your project root
2. Find this line:
   ```
   GOOGLE_API_KEY=your-google-api-key-here
   ```
3. Replace `your-google-api-key-here` with your actual key:
   ```
   GOOGLE_API_KEY=AIzaSyD1234567890abcdefghijklmnopqr
   ```
4. **Save the file**

### Step 3: Update Python Packages

Install the Google Generative AI package:

```bash
pip install -r requirements.txt
```

Or directly:

```bash
pip install google-generativeai>=0.3.0
```

### Step 4: Restart Django Server

If the server is running, restart it to load the new configuration:

```bash
# In VS Code terminal, press Ctrl+C to stop, then:
python manage.py runserver
```

### Step 5: Test the Chat 🎉

1. Open http://127.0.0.1:8000/ in your browser
2. Click the **gold chat button** (✦) in the bottom-right corner
3. Ask Aria a question like:
   - "Tell me about summer vacation packages"
   - "What beach destinations do you recommend?"
   - "I'm looking for an adventure trip"

You should see Aria respond with travel recommendations!

---

## 🛠️ Troubleshooting

### Chat button shows but no response
**Problem**: GOOGLE_API_KEY not set correctly
**Solution**: 
1. Verify `.env` file syntax (no quotes around key)
2. Check key starts with `AIzaSy`
3. Restart Django server

### "API configuration error" message
**Problem**: Google API key missing or invalid
**Solution**:
1. Get new key from: https://aistudio.google.com/app/apikey
2. Paste into .env file exactly as copied
3. Restart Django server
4. Clear browser cache and reload page

### "Service temporarily unavailable"
**Problem**: Network error or API limit reached
**Solution**:
1. Check internet connection
2. Verify API key is valid on https://console.cloud.google.com
3. Check Google Cloud project has billing enabled (free tier requires no payment)
4. Wait a few moments and retry

### ImportError: google.generativeai
**Problem**: Package not installed
**Solution**:
```bash
pip install google-generativeai>=0.3.0
```

---

## 📋 API Endpoints

Your landing page automatically uses these endpoints:

### Chat Endpoint
- **URL**: `/api/chat/`
- **Method**: POST
- **Body**:
  ```json
  {
    "message": "Tell me about beach trips",
    "history": [...]
  }
  ```
- **Response**:
  ```json
  {
    "reply": "Aria's response about beach destinations..."
  }
  ```

### Booking Endpoint
- **URL**: `/api/bookings/`
- **Method**: POST
- **Body**:
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "date": "2026-05-15",
    "guests": 2,
    "package_id": 1
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "booking_id": "WL-20260331120000",
    "message": "Booking confirmed! Confirmation sent to john@example.com",
    "total": 4980
  }
  ```

---

## 💰 Pricing & Limits

**Google Gemini API Pricing**:
- **Free Tier**: 60 requests per minute (RPM)
  - Completely free, no credit card needed
  - Perfect for development and testing
  - Up to 10,000 requests per day

- **Paid Tier**: $0.075 per 1M input tokens, $0.30 per 1M output tokens
  - Each chat message ≈ 100-500 tokens
  - Estimated cost: ~$0.0001-0.001 per chat message
  - Requires valid billing
  
**Rate Limits**:
- Free tier: 60 requests per minute (plenty for small sites)
- Paid tier: 10,000 RPM standard
- Much more sustainable than other AI APIs for production use

**No Credit Card Required** for free tier! 🎉

---

## ✅ Features Included

Your landing page includes:

1. **Premium React UI**
   - Glassmorphism design
   - Smooth animations
   - Responsive mobile design
   - Gold, navy, teal color scheme

2. **AI Chatbot (Aria)**
   - Powered by Google Gemini 2.0 Flash
   - Conversational travel consultant
   - Memory of available packages
   - Warm, sophisticated tone
   - Fast responses (Flash model is optimized for speed)

3. **Booking System**
   - Real-time price calculator
   - Form validation
   - Email confirmation
   - Booking ID generation

4. **Landing Page Sections**
   - Hero section with animated stats
   - Destinations grid (6 cards)
   - Tour packages grid (6 cards)
   - How it works (3-step process)
   - Testimonials section
   - Newsletter subscription
   - Footer with links

---

## 🔄 Switching Models

To use a different Gemini model, edit `travel/api.py`:

```python
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",  # Change this line
    system_instruction=SYSTEM_PROMPT
)
```

**Available Models**:
- `gemini-2.0-flash` (recommended - fast & cheap)
- `gemini-1.5-pro` (more powerful but slower)
- `gemini-1.5-flash` (lighter version)

---

## 📞 Support

- **Google AI Studio**: https://aistudio.google.com
- **API Documentation**: https://ai.google.dev
- **Get API Key**: https://aistudio.google.com/app/apikey
- **Status/Issues**: https://issuetracker.google.com/issues?q=componentid:187172

---

## 🎯 Why Gemini?

✅ **Free tier** - No credit card required for development
✅ **Fast** - Gemini 2.0 Flash optimized for speed
✅ **Reliable** - Google's infrastructure
✅ **Cost-effective** - Competitive pricing for production
✅ **Easy setup** - Just copy and paste your API key
✅ **Great for travel AI** - Excellent at understanding travel queries

---

**Status**: Ready for testing! 🚀
