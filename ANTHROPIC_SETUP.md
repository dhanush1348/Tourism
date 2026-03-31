# ✨ Anthropic Claude API Setup Guide

## 🚀 Quick Setup (5 minutes)

Your premium landing page with Aria (AI chatbot) is almost ready! Follow these steps to activate the chat functionality.

### Step 1: Get Your Anthropic API Key

1. **Create a free account** at https://console.anthropic.com
   - Sign up with email or Google/GitHub account
   - Verify your email
   
2. **Navigate to API Keys**
   - Go to: https://console.anthropic.com/account/keys
   - Click the **"Create Key"** button
   - Copy the key (starts with `sk-ant-`)

### Step 2: Add Key to .env File

1. Open `.env` file in your project root
2. Find this line:
   ```
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   ```
3. Replace `sk-ant-your-key-here` with your actual key:
   ```
   ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxx
   ```
4. **Save the file**

### Step 3: Restart Django Server

If the server is running, it will auto-reload with the new environment variable:

```bash
# In VS Code terminal, press Ctrl+C to stop, then:
python manage.py runserver
```

### Step 4: Test the Chat 🎉

1. Open http://127.0.0.1:8000/ in your browser
2. Click the **gold chat button** (✦) in the bottom-right corner
3. Ask Aria a question like:
   - "Tell me about beach destinations"
   - "What packages do you offer?"
   - "I want a luxury experience"

You should see Aria respond with travel recommendations!

---

## 🛠️ Troubleshooting

### Chat button shows but no response
**Problem**: ANTHROPIC_API_KEY not set correctly
**Solution**: 
1. Verify `.env` file syntax (no quotes around key)
2. Check key starts with `sk-ant-`
3. Restart Django server

### "API key not found" error
**Problem**: Django can't read the .env file
**Solution**:
1. Ensure `.env` file is in project root: `c:\Users\DHANUSH\tours_project\.env`
2. Restart Django server: `python manage.py runserver`

### No response from Aria
**Problem**: Network or API error
**Solution**:
1. Check internet connection
2. Verify API key is valid on https://console.anthropic.com
3. Check Django logs for errors

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
    "booking_id": "WL-20260330120000",
    "message": "Booking confirmed! Confirmation sent to john@example.com",
    "total": 4980
  }
  ```

---

## 🔒 Pricing & Limits

**Anthropic Claude API Pricing**:
- Claude 3.5 Sonnet: $3 per 1M input tokens, $15 per 1M output tokens
- Each chat message ≈ 100-500 tokens
- Each response ≈ 100-500 tokens
- **Estimated cost**: ~$0.001 per chat message for typical queries

**Free Tier**: 
- $5 free credits for testing (expires in 3 months)
- Pay-as-you-go after that

**Rate Limits**:
- Standard tier: 10,000 requests per minute (RPM)
- More than enough for small-to-medium traffic

---

## ✅ Features Included

Your landing page includes:

1. **Premium React UI**
   - Glassmorphism design
   - Smooth animations
   - Responsive mobile design
   - Gold, navy, teal color scheme

2. **AI Chatbot (Aria)**
   - Powered by Claude 3.5 Sonnet
   - Conversational travel consultant
   - Memory of available packages
   - Warm, sophisticated tone

3. **Booking System**
   - Real-time price calculator
   - Form validation
   - Email confirmation
   - Booking ID generation

4. **Landing Page Sections**
   - Hero section with stats
   - Destinations grid (6 cards)
   - Tour packages grid (6 cards)
   - How it works (3-step process)
   - Testimonials section
   - Newsletter subscription
   - Footer with links

---

## 📞 Support

- **Anthropic Docs**: https://docs.anthropic.com
- **API Status**: https://status.anthropic.com
- **Help Console**: https://console.anthropic.com/account/login

---

**Status**: Ready for testing! 🚀
