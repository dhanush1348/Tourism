# 🚀 Deploy to Heroku - Quick Checklist

> Note (April 2026): Heroku app hosting is not free-tier for always-on deployment. Account verification and a paid plan are required before `heroku create` works.

**Time Required**: 15 minutes  
**Status**: All files prepared ✅

---

## 📋 Quick Steps

### 1️⃣ Install & Login (2 min)
```bash
# Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
heroku login
```

### 2️⃣ Create Heroku App (1 min)
```bash
heroku create wanderlust-tours
```
*(Replace with your desired app name - must be unique)*

### 3️⃣ Add PostgreSQL Database (1 min)
```bash
heroku addons:create heroku-postgresql:hobby-dev --app wanderlust-tours
```

### 4️⃣ Set Environment Variables (2 min)

**Option A - One command:**
```bash
heroku config:set \
  ENVIRONMENT=production \
  DEBUG=False \
  SECRET_KEY="$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')" \
  GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY \
  ALLOWED_HOSTS="wanderlust-tours.herokuapp.com,yourdomain.com" \
  SECURE_SSL_REDIRECT=True \
  SESSION_COOKIE_SECURE=True \
  CSRF_COOKIE_SECURE=True \
  --app wanderlust-tours
```

**Option B - Individual commands (if above fails):**
```bash
heroku config:set ENVIRONMENT=production --app wanderlust-tours
heroku config:set DEBUG=False --app wanderlust-tours
heroku config:set GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY --app wanderlust-tours
heroku config:set ALLOWED_HOSTS="wanderlust-tours.herokuapp.com,yourdomain.com" --app wanderlust-tours
heroku config:set SECURE_SSL_REDIRECT=True --app wanderlust-tours
heroku config:set SESSION_COOKIE_SECURE=True --app wanderlust-tours
heroku config:set CSRF_COOKIE_SECURE=True --app wanderlust-tours
```

### 5️⃣ Deploy Code (5 min)
```bash
# Ensure you're in the project directory
cd c:\Users\DHANUSH\tours_project

# Initialize git (if not done)
git init
git add .
git commit -m "Deployment to Heroku"

# Deploy
git push heroku main
# (or: git push heroku master - if using master branch)
```

Watch the logs during deployment - wait for "Launching... done" message.

### 6️⃣ Run Migrations (2 min)
```bash
heroku run python manage.py migrate --app wanderlust-tours
```

### 7️⃣ Test Live (1 min)
```bash
heroku open --app wanderlust-tours
```

Visit these URLs to test:
- **Landing**: https://wanderlust-tours.herokuapp.com/
- **Chat**: Click gold button (✦) and test messages
- **Booking**: Click "Book Now" on any package

---

## 🎯 Connect Custom Domain (Optional)

### In Heroku Console:
```bash
heroku domains:add yourdomain.com --app wanderlust-tours
heroku domains:add www.yourdomain.com --app wanderlust-tours
```

### In Your Domain Registrar (GoDaddy, Namecheap, etc.):

Find **CNAME Records** section and add:
```
Name: @             Value: wanderlust-tours.herokuapp.com   Type: CNAME
Name: www           Value: wanderlust-tours.herokuapp.com   Type: CNAME
```

Save and wait 24 hours for DNS to propagate.

### Update Heroku:
```bash
heroku config:set ALLOWED_HOSTS="wanderlust-tours.herokuapp.com,yourdomain.com,www.yourdomain.com" --app wanderlust-tours
```

---

## ✅ Verification Checklist

| Step | Command | Expected Result |
|------|---------|-----------------|
| Login | `heroku login` | Browser opens ✅ |
| App created | `heroku apps:list` | App appears ✅ |
| Database | `heroku config --app wanderlust-tours \| grep DATABASE` | DATABASE_URL shown ✅ |
| Deployed | `heroku logs --tail --app wanderlust-tours` | No errors ✅ |
| Live | Visit app URL | Landing page loads ✅ |
| Chat works | Click chat button | Can send messages ✅ |
| Booking works | Click "Book Now" | Can create booking ✅ |

---

## 🆘 If Something Goes Wrong

### Check Logs:
```bash
heroku logs --tail --app wanderlust-tours
```

### Restart App:
```bash
heroku restart --app wanderlust-tours
```

### Check Status:
```bash
heroku status
heroku ps --app wanderlust-tours
```

### Nuke & Redeploy:
```bash
heroku destroy --app wanderlust-tours --confirm=wanderlust-tours
# Then start from Step 2
```

---

## 📌 Important Notes

⚠️ **Custom Domain Name:**  
Replace `wanderlust-tours` with your desired name (must be unique)

⚠️ **ALLOWED_HOSTS:**  
Update with your actual domain name before deploying

⚠️ **Free Tier Limits:**
- Heroku requires account verification and paid resources for deployment
- Billing details are typically required before creating apps
- Check current pricing in Heroku dashboard before launch

🔒 **Security:**
- SSL/HTTPS automatic ✅
- All security headers configured ✅
- Database encrypted ✅

💬 **Chatbot:**
- Free tier quota: 60 requests/min
- Fallback system handles quota gracefully (no errors to users)
- Works indefinitely on free tier ✅

---

## 📚 Full Documentation

For detailed information, see:
- **[HEROKU_DEPLOYMENT_GUIDE.md](HEROKU_DEPLOYMENT_GUIDE.md)** - Complete guide with troubleshooting
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - General deployment info
- **[LAUNCH_CHECKLIST.md](LAUNCH_CHECKLIST.md)** - Pre-launch requirements

---

**Status**: Ready to deploy ✅  
**Files Created**: Procfile, runtime.txt, HEROKU_DEPLOYMENT_GUIDE.md  
**Estimated Time**: 15 minutes to go live
