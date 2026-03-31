# 🚀 QUICK START - Google Gemini Chatbot Setup

## 3 Steps to Get Your AI Chatbot Working

### Step 1️⃣: Get API Key (2 min)
```
👉 Go to: https://aistudio.google.com/app/apikey
👉 Click "Create API Key"
👉 Copy your key (starts with AIzaSy)
```

### Step 2️⃣: Update .env File (1 min)
```
Open: c:\Users\DHANUSH\tours_project\.env

Find this line:
    GOOGLE_API_KEY=your-google-api-key-here

Replace with your actual key:
    GOOGLE_API_KEY=AIzaSyD1234567890abcdefghijk...

Save the file!
```

### Step 3️⃣: Restart & Test (2 min)
```bash
# In terminal, press Ctrl+C to stop current server, then:
python manage.py runserver

# In browser, open:
http://127.0.0.1:8000/

# Click the gold chat button (✦) and ask:
"Tell me about beach vacations"
```

---

## ✅ Verification Checklist

- [ ] Got API key from Google AI Studio
- [ ] Added GOOGLE_API_KEY to .env
- [ ] Restarted Django server
- [ ] Opened http://127.0.0.1:8000/ in browser
- [ ] Clicked chat button (✦)
- [ ] Asked Aria a travel question
- [ ] Received response from AI

---

## 📊 What Changed?

| Before | After |
|--------|-------|
| Anthropic Claude API | Google Gemini API |
| `ANTHROPIC_API_KEY` | `GOOGLE_API_KEY` |
| `sk-ant-...` keys | `AIzaSy...` keys |
| anthropic package | google-generativeai |
| Command: `/api/chat/` | Same endpoint ✅ |

---

## 💡 Why Gemini?

✅ **FREE** - 60 requests/min free tier (no credit card needed!)
✅ **CHEAP** - 15-30% less expensive than Claude
✅ **FAST** - Optimized for quick responses
✅ **EASY** - Simple setup in 3 steps

---

## 🔧 Troubleshooting

**Chat button doesn't work?**
→ Check .env has correct GOOGLE_API_KEY
→ Restart server (Ctrl+C, then `python manage.py runserver`)

**"API error" message?**
→ Verify key is correct at https://aistudio.google.com/app/apikey
→ Try creating a new key

**Still not working?**
→ Run: `python test_api.py` to diagnose issues

---

## 📚 Full Documentation

- **Complete Setup Guide**: See [GEMINI_SETUP.md](GEMINI_SETUP.md)
- **Technical Details**: See [MIGRATION_CLAUDE_TO_GEMINI.md](MIGRATION_CLAUDE_TO_GEMINI.md)
- **API Testing**: Run `python test_api.py`

---

## 🎯 Features Working

✅ Chat with Aria (AI travel concierge)
✅ Book tours with price calculator
✅ View destinations & packages
✅ Email booking confirmations
✅ Newsletter signup
✅ Mobile responsive design

---

**Time to setup: ~5 minutes**
**Cost to run: FREE (for development) or $0.001/chat (production)**

🚀 Ready to go! Get your API key now → https://aistudio.google.com/app/apikey
