# 🚀 Heroku Deployment Guide - Wanderlust Tours

## Overview

Deploy your Django travel booking platform to Heroku in **15 minutes**. This guide covers production-ready setup with PostgreSQL, static files, security, and custom domain configuration.

---

## ✅ Prerequisites

### Required
- ✅ GitHub account (for easy deployment)
- ✅ Heroku account (free tier available)
- ✅ Heroku CLI installed
- ✅ Git installed
- ✅ Google API key (for Aria chatbot) - already have ✅
- ✅ Custom domain (if using one)

### Install Heroku CLI

**Windows:**
```bash
# Download and install from https://devcenter.heroku.com/articles/heroku-cli
# OR use Chocolatey
choco install heroku-cli
```

**Verify installation:**
```bash
heroku --version
```

---

## 📋 Step 1: Prepare Your App (Already Done ✅)

Your app is ready! Verify these files exist:

```
✅ Procfile          (how to start the server)
✅ runtime.txt       (Python version)
✅ requirements.txt  (all dependencies)
✅ manage.py         (Django entry point)
```

All files are present in your project.

---

## 🔑 Step 2: Heroku Setup

### Login to Heroku
```bash
heroku login
```
Browser will open - authenticate with your Heroku account.

### Create a Heroku App
```bash
heroku create wanderlust-tours
```

**Expected Output:**
```
Creating ⬢ wanderlust-tours... done
https://wanderlust-tours.herokuapp.com/ | https://git.heroku.com/wanderlust-tours.git
```

**Note**: Replace `wanderlust-tours` with your desired app name (must be unique).

### Verify App Created
```bash
heroku apps:list
```

---

## 🗄️ Step 3: PostgreSQL Database

Heroku provides free PostgreSQL!

### Add PostgreSQL to Your App
```bash
heroku addons:create heroku-postgresql:hobby-dev --app wanderlust-tours
```

**Expected Output:**
```
Creating heroku-postgresql:hobby-dev on ⬢ wanderlust-tours... free
PostgreSQL has been created and is available as DATABASE_URL
```

### Verify Database
```bash
heroku config --app wanderlust-tours
```

You'll see `DATABASE_URL` variable automatically added.

---

## 🔐 Step 4: Set Environment Variables

These variables control your app behavior in production.

### Set All Required Variables
```bash
# Essential Variables
heroku config:set ENVIRONMENT=production \
  --app wanderlust-tours

heroku config:set DEBUG=False \
  --app wanderlust-tours

heroku config:set SECRET_KEY="$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')" \
  --app wanderlust-tours

# Your Google API Key (from your .env file)
heroku config:set GOOGLE_API_KEY=AIzaSyDu-gZ8Rzt4_hriDIgKGRzpMmOAvs4rTbc \
  --app wanderlust-tours

# Allowed Hosts - UPDATE THIS WITH YOUR DOMAIN!
heroku config:set ALLOWED_HOSTS="wanderlust-tours.herokuapp.com,yourdomain.com" \
  --app wanderlust-tours

# Security Headers
heroku config:set SECURE_SSL_REDIRECT=True \
  --app wanderlust-tours

heroku config:set SESSION_COOKIE_SECURE=True \
  --app wanderlust-tours

heroku config:set CSRF_COOKIE_SECURE=True \
  --app wanderlust-tours
```

### Verify Variables Set
```bash
heroku config --app wanderlust-tours
```

---

## 📤 Step 5: Deploy Your App

### Initialize Git (if not already done)
```bash
git init
git add .
git commit -m "Initial deployment to Heroku"
```

### Deploy to Heroku
```bash
git push heroku main
```

**Note**: If your branch is called `master` instead of `main`, use:
```bash
git push heroku master
```

**Expected Output:**
```
Counting objects: 85, done.
...
Compressing source code... done.
...
Building source... done.
...
       Running migrations... done.
       Collectingstatic... done.
       Launching... done, v3
       https://wanderlust-tours.herokuapp.com/ deployed to Heroku
```

### Monitor Deployment
```bash
heroku logs --tail --app wanderlust-tours
```

---

## ✨ Step 6: Run Initial Setup

### Create Superuser (Admin Account)
```bash
heroku run python manage.py createsuperuser --app wanderlust-tours
```

This is **optional** but recommended for admin panel access.

### Load Sample Data (Optional)
```bash
heroku run python manage.py create_sample_data --app wanderlust-tours
```

### Run Database Migrations
```bash
heroku run python manage.py migrate --app wanderlust-tours
```

---

## 🌐 Step 7: Test Live App

### Open Your App
```bash
heroku open --app wanderlust-tours
```

Or visit: `https://wanderlust-tours.herokuapp.com/`

**Test endpoints:**
- Landing page: `https://wanderlust-tours.herokuapp.com/`
- Chat API: `POST` to `/api/chat/`
- Booking API: `POST` to `/api/bookings/`
- Admin: `https://wanderlust-tours.herokuapp.com/admin/`

---

## 🎯 Step 8: Connect Custom Domain (If You Have One)

### Prerequisites
- Custom domain registered (GoDaddy, Namecheap, etc.)
- Access to domain DNS settings

### Add Domain to Heroku App
```bash
heroku domains:add yourdomain.com --app wanderlust-tours
heroku domains:add www.yourdomain.com --app wanderlust-tours
```

### Configure DNS

Your domain registrar should show:
```
DNS Records needed for Heroku:

Host: yourdomain.com
Value: wanderlust-tours.herokuapp.com
Type: CNAME (or ALIAS)

Host: www.yourdomain.com
Value: wanderlust-tours.herokuapp.com
Type: CNAME
```

**Example (GoDaddy):**
1. Go to DNS Management
2. Find CNAME records section
3. Add:
   - Name: `@` (or yourdomain.com)
   - Value: `wanderlust-tours.herokuapp.com`
   - Name: `www`
   - Value: `wanderlust-tours.herokuapp.com`
4. Save changes (may take 24 hours to propagate)

### Update ALLOWED_HOSTS in Heroku
```bash
heroku config:set ALLOWED_HOSTS="wanderlust-tours.herokuapp.com,yourdomain.com,www.yourdomain.com" \
  --app wanderlust-tours
```

### Verify Domain Connected
```bash
heroku domains --app wanderlust-tours
```

---

## 🔒 SSL/HTTPS Certificate (Automatic)

Heroku automatically provisions **Let's Encrypt SSL** for your app!

✅ Your app is secure by default on Heroku.

Check certificate:
```bash
heroku certs --app wanderlust-tours
```

---

## 📊 Step 9: Monitor Your App

### View Live Logs
```bash
# Last 100 lines
heroku logs --num 100 --app wanderlust-tours

# Real-time log stream
heroku logs --tail --app wanderlust-tours
```

### Monitor Resource Usage
```bash
heroku ps --app wanderlust-tours
heroku ps:scale web=1 --app wanderlust-tours
```

### Check Dyno Hours
```bash
heroku account:whoami
heroku apps:info --app wanderlust-tours
```

---

## 🚨 Troubleshooting

### App Won't Start
```bash
heroku logs --tail --app wanderlust-tours
```
Look for errors in the log output.

### Database Connection Error
```bash
# Verify DATABASE_URL is set
heroku config --app wanderlust-tours | grep DATABASE_URL

# Run migrations
heroku run python manage.py migrate --app wanderlust-tours
```

### Static Files Not Loading (White page)
```bash
# Collect static files
heroku run python manage.py collectstatic --app wanderlust-tours

# Clear Heroku cache and redeploy
heroku builds:cancel --app wanderlust-tours
git push heroku main --force
```

### Too Many Requests / Quota Error
Your Gemini API might have quota exhausted.
- Check Google Cloud Console
- Upgrade to paid tier if needed
- Or relay on fallback responses (no error shown to users)

### Custom Domain Not Working
```bash
# Check DNS propagation (wait up to 24 hours)
# Use online tool: https://mxtoolbox.com/

# Verify Heroku domains
heroku domains --app wanderlust-tours

# Check CNAME records
nslookup yourdomain.com
```

---

## ⚡ Common Commands Reference

```bash
# Deployment
git push heroku main                          # Deploy latest code
heroku open --app wanderlust-tours           # Open app in browser
heroku logs --tail --app wanderlust-tours    # View live logs

# Configuration
heroku config --app wanderlust-tours         # View all config vars
heroku config:set KEY=value --app wanderlust-tours  # Set variable
heroku config:unset KEY --app wanderlust-tours     # Delete variable

# Database
heroku pg:info --app wanderlust-tours        # Database details
heroku pg:backups --app wanderlust-tours     # Database backups

# Running Commands
heroku run python manage.py migrate --app wanderlust-tours
heroku run python manage.py createsuperuser --app wanderlust-tours
heroku ps --app wanderlust-tours             # View running dynos

# Monitoring
heroku status                                 # Heroku system status
heroku apps:info --app wanderlust-tours      # App information
heroku ps:scale web=2 --app wanderlust-tours # Scale to 2 dynos (costs $7/month)
```

---

## 📈 Scaling Options

| Option | Cost | When to Use |
|--------|------|-----------|
| Free Tier | $0/month | Testing, demos, low traffic |
| Hobby Dyno | $7/month | Small production app |
| Standard 1X | $25/month | Production app |
| Standard 2X | $50/month | High traffic |

Your app starts on free tier dyno, which sleeps after 30 min of inactivity.

To upgrade:
```bash
heroku ps:scale web=1:standard-1x --app wanderlust-tours
```

---

## 💰 Free & Paid Tier Limits

### Free PostgreSQL Database (Hobby Dev)
- ✅ 10,000 rows max
- ✅ Free SSL
- ✅ Daily backups
- ✅ No cost!

### Free Dyno (Web Server)
- ✅ 550 dyno hours/month (sleeps after 30 min)
- ✅ Perfect for testing
- Later: Upgrade to paid for always-on

### Google Gemini API
- ✅ Your custom key
- Free tier: 60 requests/min
- Chat has fallback system (works on free tier forever!)

---

## ✅ Post-Deployment Checklist

- [ ] App is running: `https://wanderlust-tours.herokuapp.com/`
- [ ] Database connected (no connection errors in logs)
- [ ] Chat endpoint working (`/api/chat/`)
- [ ] Booking endpoint working (`/api/bookings/`)
- [ ] Static files loading (CSS/JS styling visible)
- [ ] Email configured (optional)
- [ ] Custom domain connected (if applicable)
- [ ] SSL certificate active (automatic)
- [ ] Admin superuser created (optional)
- [ ] Logs monitored for errors

---

## 🎉 Success!

Your Wanderlust Tours platform is now **LIVE on the internet!** 

### Next Steps
1. Share the URL with users: `yourdomain.com`
2. Monitor logs regularly: `heroku logs --tail`
3. Backup database periodically: `heroku pg:backups:capture`
4. Update ALLOWED_HOSTS if adding more domains

---

## 📞 Quick Support

**Heroku Status**: https://status.heroku.com/
**Django Docs**: https://docs.djangoproject.com/
**Heroku Help**: https://help.heroku.com/

**Check app status:**
```bash
heroku apps:info --app wanderlust-tours
```

---

**Last Updated**: April 1, 2026  
**Status**: Ready for Production ✅  
**Estimated Deployment Time**: 15 minutes
