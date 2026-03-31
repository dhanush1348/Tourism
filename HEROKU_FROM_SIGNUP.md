# 🚀 Heroku Deployment - Complete Guide from Signup

**Total Time**: 20-30 minutes  
**Difficulty**: Easy (just follow along!)  
**No Prior Experience Needed**: ✅

---

## 📝 Step 1: Create Heroku Account (2 minutes)

### 1a. Go to Heroku Website
Open: https://www.heroku.com/

### 1b. Click "Sign Up"
- Enter your email
- Create a password
- Select "Developer" (free account)
- Click "Create Free Account"

### 1c. Verify Email
Check your email for verification link from Heroku.
Click the link to verify your account.

### 1d. Set Up Your Account
- Accept terms
- Create password
- You're ready! ✅

---

## 💻 Step 2: Install Heroku CLI (3 minutes)

The Heroku CLI is a command-line tool that lets you manage your app from your computer.

### 2a. Download Heroku CLI

**For Windows:**
1. Go to: https://devcenter.heroku.com/articles/heroku-cli
2. Find the **Windows** section
3. Click download for your system (64-bit)
4. Run the installer (.exe file)
5. Follow the installation wizard (click Next, Agree, Install)

**Using Chocolatey (if you have it):**
```bash
choco install heroku-cli
```

### 2b. Verify Installation
Open PowerShell or Command Prompt and type:
```bash
heroku --version
```

**Expected output:**
```
heroku/8.1.8 win32-x64 node-v18.14.0
```

If you see a version number, you're good! ✅

### 2c. Troubleshooting Installation
If `heroku` command not found:
- Restart your computer (required after installation)
- Or open a new PowerShell window

---

## 🔐 Step 3: Login to Heroku from Command Line (2 minutes)

### 3a. Open PowerShell
1. Press `Win + R`
2. Type `powershell`
3. Press Enter

### 3b. Navigate to Your Project
```bash
cd c:\Users\DHANUSH\tours_project
```

### 3c. Login to Heroku
```bash
heroku login
```

**What happens:**
- Your browser opens automatically
- Click "Log In" button
- You're logged in!
- Return to PowerShell (it will show success message)

---

## 📦 Step 4: Create Your Heroku App (2 minutes)

### 4a. Create the App
```bash
heroku create my-wanderlust-app
```

**Replace `my-wanderlust-app` with:**
- Your desired app name
- Must be unique (no spaces, lowercase, hyphens okay)
- Examples: `wanderlust-tours-2026`, `tours-booking-app`

**Expected output:**
```
Creating ⬢ my-wanderlust-app... done
https://my-wanderlust-app.herokuapp.com/ | https://git.heroku.com/my-wanderlust-app.git
Updating remotes in cloud... done
heroku/main is set as the default remote
```

**Note down your app URL**: `https://my-wanderlust-app.herokuapp.com/`

### 4b. Verify App Created
```bash
heroku apps
```

You should see your app listed.

---

## 🗄️ Step 5: Add PostgreSQL Database (2 minutes)

Heroku provides a free PostgreSQL database!

### 5a. Add Database Addon
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

**Expected output:**
```
Creating heroku-postgresql:hobby-dev on ⬢ my-wanderlust-app... free
PostgreSQL has been created and is available as DATABASE_URL
```

### 5b. Verify Database Created
```bash
heroku config
```

You should see `DATABASE_URL` in the output.

---

## 🔑 Step 6: Set Environment Variables (5 minutes)

These are settings that control how your app behaves.

### 6a. Generate Secret Key
Run this command to generate a random secret key:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output (long random string).

### 6b. Set All Variables (Option A - Easiest)

Copy and paste this entire command (one at a time):

```bash
heroku config:set ENVIRONMENT=production
```

Then:
```bash
heroku config:set DEBUG=False
```

Then:
```bash
heroku config:set SECRET_KEY="<paste-your-random-key-here>"
```

Then:
```bash
heroku config:set GOOGLE_API_KEY=AIzaSyDu-gZ8Rzt4_hriDIgKGRzpMmOAvs4rTbc
```

Then:
```bash
heroku config:set ALLOWED_HOSTS="my-wanderlust-app.herokuapp.com"
```

Then:
```bash
heroku config:set SECURE_SSL_REDIRECT=True
```

Then:
```bash
heroku config:set SESSION_COOKIE_SECURE=True
```

Then:
```bash
heroku config:set CSRF_COOKIE_SECURE=True
```

### 6c. Verify All Variables Set
```bash
heroku config
```

**You should see:**
```
=== my-wanderlust-app Config Vars
ALLOWED_HOSTS:           my-wanderlust-app.herokuapp.com
CSRF_COOKIE_SECURE:      True
DEBUG:                   False
ENVIRONMENT:             production
GOOGLE_API_KEY:          AIzaSyDu-gZ8Rzt4_hriDIgKGRzpMmOAvs4rTbc
SECRET_KEY:              <your-random-key>
SESSION_COOKIE_SECURE:   True
```

All 7 variables should be there! ✅

---

## 📤 Step 7: Deploy Your Code (5 minutes)

### 7a. Check if Git is Initialized
```bash
git status
```

**If you see an error** "fatal: not a git repository":
```bash
git init
```

### 7b. Add All Files
```bash
git add .
```

### 7c. Commit Your Code
```bash
git commit -m "Initial deployment to Heroku"
```

**Expected output:**
```
[main (root-commit) a1b2c3d] Initial deployment to Heroku
 XX files changed, XXXX insertions(+)
 ...
```

### 7d. Deploy to Heroku
```bash
git push heroku main
```

**This will:**
1. Upload your code to Heroku
2. Install Python dependencies
3. Run your migrations
4. Start your app

**Watch for:** "Launching... done" message

**Expected final output:**
```
remote:        Launching... done, v3
remote: https://my-wanderlust-app.herokuapp.com/ deployed to Heroku
```

---

## 🗄️ Step 8: Run Database Migrations (2 minutes)

### 8a. Run Migrations
```bash
heroku run python manage.py migrate
```

**Expected output:**
```
Running python manage.py migrate on ⬢ my-wanderlust-app... up, run.1234
Operations to perform:
  ...
Running migrations... Done
```

### 8b. Create Admin Account (Optional but Recommended)
```bash
heroku run python manage.py createsuperuser
```

Follow the prompts:
- Username: `admin`
- Email: your-email@example.com
- Password: choose a strong password
- Confirm: repeat password

---

## ✨ Step 9: Test Your Live App (2 minutes)

### 9a. Open Your App
```bash
heroku open
```

Your app opens in browser! You should see the landing page. ✅

### 9b. Test the Chat
1. Click the gold chat button (✦) in bottom right
2. Type: "Tell me about beaches"
3. Should get a response ✅

### 9c. Test Booking
1. Click "Book Now" on any package
2. Fill out the form:
   - Name: Your name
   - Email: your@email.com
   - Date: 2026-05-15
   - Guests: 2
   - Package: Select one
3. Click "Confirm Booking"
4. Should see success message ✅

---

## 🌐 Step 10: Add Custom Domain (Optional, 5 minutes)

Only do this if you have your own domain!

### 10a. Add Domain to Heroku
```bash
heroku domains:add yourdomain.com
heroku domains:add www.yourdomain.com
```

Example: If your domain is `mytours.com`:
```bash
heroku domains:add mytours.com
heroku domains:add www.mytours.com
```

**Expected output:**
```
⬢ my-wanderlust-app
Domain Name            DNS Target
━━━━━━━━━━━━━━━━━━━━━ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
yourdomain.com         my-wanderlust-app.herokuapp.com
```

### 10b. Update Domain DNS Settings

Go to your domain registrar (GoDaddy, Namecheap, etc.):

1. Find "DNS Management" or "Domain Settings"
2. Look for "CNAME Records" section
3. Add/Edit these records:

```
Host: @              Value: my-wanderlust-app.herokuapp.com   Type: CNAME
Host: www            Value: my-wanderlust-app.herokuapp.com   Type: CNAME
```

**Example for GoDaddy:**
- Go to DNS
- Find "Manage CNAME" or "CNAME Records"
- Set Name: `@` → Value: `my-wanderlust-app.herokuapp.com`
- Set Name: `www` → Value: `my-wanderlust-app.herokuapp.com`
- Save

### 10c. Update Heroku Allowed Hosts
```bash
heroku config:set ALLOWED_HOSTS="my-wanderlust-app.herokuapp.com,yourdomain.com,www.yourdomain.com"
```

### 10d. Wait for DNS
DNS changes take 24-48 hours to fully propagate.
Your domain will work at: `https://yourdomain.com`

---

## ✅ Success Checklist

| Step | Check | Status |
|------|-------|--------|
| 1. Heroku account created | Can login at heroku.com | ✅ |
| 2. Heroku CLI installed | `heroku --version` shows version | ✅ |
| 3. Logged in | `heroku auth:whoami` shows email | ✅ |
| 4. App created | `heroku apps` shows app name | ✅ |
| 5. Database added | `heroku config` shows DATABASE_URL | ✅ |
| 6. Variables set | `heroku config` shows 7 variables | ✅ |
| 7. Code deployed | See "Launching... done" | ✅ |
| 8. Migrations run | `heroku logs` shows migrations complete | ✅ |
| 9. App works | Landing page loads | ✅ |
| 10. Chat works | Can send messages | ✅ |
| 11. Booking works | Can create booking | ✅ |

---

## 🆘 Troubleshooting

### "heroku: command not found"
- Restart your PowerShell window (close and reopen)
- Or restart your computer

### "app already exists"
Name is taken. Choose a different name:
```bash
heroku create my-wanderlust-app-2026
```

### "Launching failed"
Check logs:
```bash
heroku logs --tail
```
Read the error message and scroll up to find the issue.

### "Database connection error"
Run migrations again:
```bash
heroku run python manage.py migrate
```

### Landing page loads but chat/booking don't work
Check logs:
```bash
heroku logs --tail
```
Look for error messages.

### Static files not showing (styling broken)
```bash
heroku run python manage.py collectstatic --noinput
```

### Restart/Redeploy Everything
```bash
heroku restart
```

Or redeploy code:
```bash
git add .
git commit -m "Update"
git push heroku main
```

---

## 📊 Monitor Your App

### View Logs (Last 100 lines)
```bash
heroku logs --num 100
```

### View Live Logs (Real-time)
```bash
heroku logs --tail
```
(Press Ctrl+C to stop)

### Check App Status
```bash
heroku status
heroku apps:info
```

### View Active Dynos
```bash
heroku ps
```

---

## 🔄 Making Updates

After you make changes to your code locally:

```bash
# Step 1: Commit changes
git add .
git commit -m "Update description"

# Step 2: Deploy
git push heroku main

# Step 3: Check logs
heroku logs --tail
```

---

## 💰 Pricing (Free to Start!)

### Free Tier Includes:
- ✅ App server (sleeps after 30 min of inactivity)
- ✅ PostgreSQL database (10,000 rows)
- ✅ 550 hours/month (runs free app)
- ✅ SSL/HTTPS certificate
- ✅ Custom domain support (domain costs extra, not Heroku)

### Costs When You Scale:
- Always-on server: $7-50/month
- More database rows: $50+/month
- These are optional upgrades

**Your app starts free!** Pay nothing until you're ready to scale.

---

## 🎯 Quick Reference Commands

```bash
# Basics
heroku login                           # Login
heroku create app-name                 # Create app
heroku open                            # Open app in browser
heroku destroy --app app-name          # Delete app (careful!)

# Configuration  
heroku config                          # View all variables
heroku config:set KEY=value            # Set a variable
heroku config:unset KEY                # Delete a variable

# Database
heroku addons:create heroku-postgresql:hobby-dev  # Add database
heroku pg:info                         # Database details

# Deployment
git push heroku main                   # Deploy code
heroku run python manage.py migrate    # Run migrations

# Monitoring
heroku logs --tail                     # Live logs
heroku logs --num 100                  # Last 100 lines
heroku ps                              # Running processes

# Users
heroku run python manage.py createsuperuser  # Create admin
```

---

## 📌 Important Notes

⚠️ **App Name is Your Subdomain:**
- App name: `my-wanderlust-app`
- URL: `https://my-wanderlust-app.herokuapp.com`

⚠️ **Free Tier Apps Sleep:**
- After 30 minutes of no activity
- First request wakes it up (5-10 second delay)
- Upgrade to paid dyno for always-on

⚠️ **Database Size:**
- 10,000 rows free
- Expand when you have more bookings

⚠️ **Keep Secrets Secret:**
- Never put API keys in code
- Always use `heroku config:set`
- Your `.env` file is in `.gitignore` (not uploaded)

---

## 🎉 Congratulations!

Your app is now **LIVE on the internet!** 🚀

**Your URL**: https://my-wanderlust-app.herokuapp.com/

Share this URL and people can:
- View your landing page
- Chat with Aria (AI assistant)
- Book travel packages
- All from their browser!

---

## 📚 Next Steps

1. **Monitor logs regularly**: `heroku logs --tail`
2. **Backup database**: `heroku pg:backups:capture`
3. **Update your code**: Make changes locally, then `git push heroku main`
4. **Upgrade when needed**: When free tier doesn't match your needs
5. **Add custom domain**: Point your domain DNS to Heroku

---

**Total Time Spent**: 20-30 minutes  
**Your App**: LIVE ✅  
**Next Update**: Takes 1 minute (just push to git!)

Need help? Check:
- Heroku Docs: https://devcenter.heroku.com/
- Django Docs: https://docs.djangoproject.com/
- Your app logs: `heroku logs --tail`

---

**Last Updated**: April 1, 2026  
**Status**: Ready for Production ✅
