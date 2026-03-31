# ⚙️ QA Test Environment Setup Guide
## Tourism Recommendation System | Pre-Testing Checklist

**Version**: 1.0  
**Last Updated**: March 30, 2026  
**For**: QA Team Setup Instructions

---

## 📋 Pre-Testing Environment Setup Checklist

### Part 1: Clone Repository & Dependencies (15 minutes)

```bash
# Step 1: Clone the repository
git clone https://github.com/[your-org]/wanderlust-tours.git
cd wanderlust-tours

# Step 2: Create virtual environment
python -m venv venv

# Step 3: Activate virtual environment
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# Step 4: Install dependencies
pip install -r requirements.txt

# Step 5: Apply migrations
python manage.py migrate

# Step 6: Create superuser (admin account)
python manage.py createsuperuser
# Username: testadmin
# Email: admin@example.com
# Password: AdminPass123!

# Step 7: Load sample data
python manage.py create_sample_data

echo "✅ Repository & Dependencies Setup Complete"
```

**Success Indicators**:
- ✅ No errors during `pip install`
- ✅ Migrations applied successfully
- ✅ Sample data created
- ✅ Superuser created

---

### Part 2: Environment Configuration (10 minutes)

```bash
# Create .env file from template
cp .env.example .env

# Edit .env with local settings (Windows - use Notepad)
# Or edit in VS Code
code .env
```

**Required .env variables**:
```env
# Core Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-for-development
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (Development - SQLite)
DB_ENGINE=sqlite3
DB_NAME=db.sqlite3

# Redis (Optional for development)
REDIS_URL=redis://127.0.0.1:6379/0

# Email (Development - Console)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Security (Disabled for Dev)
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

**Verification**:
```bash
python manage.py check
# Output: System check identified no issues (0 silenced).
```

---

### Part 3: Database Verification (5 minutes)

```bash
# Check database connection
python manage.py dbshell

# In Python interpreter:
# .exit to quit

# Verify sample data loaded
python manage.py shell
```

```python
from travel.models import Destination, TourPackage, Booking, Review

# Check data counts
print(f"Destinations: {Destination.objects.count()}")
print(f"Tour Packages: {TourPackage.objects.count()}")
print(f"Bookings: {Booking.objects.count()}")
print(f"Reviews: {Review.objects.count()}")

# Expected output:
# Destinations: 6
# Tour Packages: 12
# Bookings: 5
# Reviews: 8

exit()
```

**Success Indicators**:
- ✅ Database connection successful
- ✅ All tables exist
- ✅ Sample data populated

---

### Part 4: Start Development Server (10 minutes)

```bash
# Terminal 1: Start Django development server
python manage.py runserver

# Expected output:
# Starting development server at http://127.0.0.1:8000/
# Quit the server with CONTROL-C.
```

### Open in Browser
```
http://localhost:8000         # Homepage
http://localhost:8000/admin   # Admin panel
```

**Login with superuser**:
- Username: `testadmin`
- Password: `AdminPass123!`

**Success Indicators**:
- ✅ Server starts without errors
- ✅ Homepage loads Successfully
- ✅ Admin panel accessible
- ✅ Can login with superuser credentials

---

## 🧪 Test Environment Validation (30 minutes)

### Quick Smoke Tests

#### Test 1: Homepage loads
```
GET http://localhost:8000/
Expected: 200 OK
Featured packages displayed: Yes
```

#### Test 2: Destination list loads
```
GET http://localhost:8000/destinations/
Expected: 200 OK, 6 destinations displayed
```

#### Test 3: Package list with filtering
```
GET http://localhost:8000/packages/?difficulty=easy
Expected: 200 OK, easy packages filtered
```

#### Test 4: Search functionality
```
GET http://localhost:8000/search/?q=Paris
Expected: 200 OK, matching results returned
```

#### Test 5: User registration
```
POST http://localhost:8000/register/
Data: username, email, password
Expected: User created, redirect to login
```

#### Test 6: User login
```
POST http://localhost:8000/login/
Data: username, password
Expected: Authenticated, redirect to home
```

**Run using Postman**:
1. Import: `Wanderlust_API_Tests.postman_collection.json`
2. Set environment variable: `base_url = http://localhost:8000`
3. Run collection (Start → Run Collection)

---

## 🛠️ Tools Setup Required for Each QA Engineer

### QA Engineer 1: API Testing Setup

#### Required Software
```
✅ Postman (Download from postman.com/downloads)
✅ CURL (Included in Windows 10+, Mac, Linux)
✅ Git (Download from git-scm.com)
✅ Python 3.11 (Download from python.org)
✅ VS Code (Download from code.visualstudio.com)
```

#### Postman Setup
```
1. Open Postman
2. Click Import
3. Import: Wanderlust_API_Tests.postman_collection.json
4. Select Environment: Development
5. Create environment variable:
   - base_url = http://localhost:8000
   - auth_token = [will be filled during testing]
6. Run collection: Collections → Wanderlust → Run
```

#### VS Code Extensions
```
- REST Client (humao.rest-client)
- Postman for VSCode (rohinijohn.postman-for-vscode)
- Thunder Client (rangav.vscode-thunder-client)
```

---

### QA Engineer 2: Functional Testing Setup

#### Required Software
```
✅ Chrome Browser (Latest version)
✅ Firefox Browser (Latest version)
✅ VS Code or DevTools
✅ Mobile testing tool (Android emulator or physical device)
```

#### Chrome DevTools Setup
```
1. Open Chrome
2. Press F12 to open DevTools
3. Go to Settings → Experiments
4. Enable all relevant experiments
5. Set device emulation for mobile testing
   - Ctrl+Shift+M to toggle device mode
```

#### Firefox DevTools
```
1. Open Firefox
2. Press F12
3. Go to Settings → Inspector
4. Enable responsive design mode (Ctrl+Shift+M)
```

#### Mobile Testing
```
Windows:
1. Download Android SDK emulator
2. Create virtual device (Pixel 5, Android 12)
3. Start emulator
4. Navigate to http://[PC-IP]:8000

Mac:
1. Download Xcode
2. Open iOS simulator
3. Navigate to http://localhost:8000

Physical Device:
1. Connect device to same network
2. Find PC IP: ipconfig getifaddr en0 (Mac) or ipconfig (Windows)
3. Navigate to http://[PC-IP]:8000
```

---

### QA Engineer 3: Performance & Security Testing Setup

#### Required Software & Tools
```
✅ Apache JMeter (jmeter.apache.org)
✅ Python 3.11
✅ pip (Python package manager)
✅ Git Bash or Terminal
```

#### JMeter Setup
```
1. Download JMeter from jmeter.apache.org
2. Extract to C:\tools\apache-jmeter (Windows) or /opt (Mac/Linux)
3. Add to PATH:
   Windows: C:\tools\apache-jmeter\bin
   Mac/Linux: /opt/apache-jmeter/bin
4. Verify: jmeter --version
```

#### Performance Testing Tools Setup
```bash
# Install performance testing libraries
pip install locust        # Load testing
pip install pytest-benchmark  # Benchmarking
pip install memory-profiler   # Memory analysis

# Verify installation
locust --version
```

#### Security Testing Tools
```bash
# Install security tools
pip install bandit        # Python security linter
pip install safety        # Python dependency checker

# Verify installation
bandit --version
safety --version

# Run security scan on project
bandit -r travel/
safety check
```

---

### QA Engineer 4: Regression & Documentation Setup

#### Required Software
```
✅ Git (for version control)
✅ VS Code (for documentation)
✅ Markdown editor or VS Code
✅ HTML/CSS editor (optional)
```

#### VS Code Extensions
```
- Markdown Preview Enhanced (shd101wyy.markdown-preview-enhanced)
- Markdown Linter (davidanson.vscode-markdownlint)
- Better Comments (aaron-bond.better-comments)
- Draw.io Integration (hediet.vscode-drawio)
```

#### Documentation Setup
```
1. Create testing notes folder: mkdir test_notes
2. Create daily test logs: touch test_notes/2026-03-30.md
3. Setup Git to track changes: git add test_notes/
4. Use this template:

# Daily Test Notes - [Date]

## Morning Plan
- [ ] [Test case 1]
- [ ] [Test case 2]

## Results
### Passed (10)
- TC-001 ✅
- TC-002 ✅

### Failed (1)
- TC-003 ❌ Browser cache issue

## Defects Found
- DEF-001: [Issue description]

## Notes
- [Any observations]
```

---

## 🌐 Multi-Environment Testing

### Development Environment (Local)
```
URL: http://localhost:8000
Database: SQLite (db.sqlite3)
Cache: In-memory cache
Admin: testadmin / AdminPass123!
Used For: Initial functional testing
```

### Docker Environment (Local Containers)
```bash
# Start all services
docker-compose up -d

# Services available:
# Django: http://localhost:8000
# Nginx: http://localhost
# PostgreSQL: localhost:5432
# Redis: localhost:6379

# View logs
docker-compose logs -f web

# Stop services
docker-compose down
```

### Staging Environment (Server)
```
URL: https://staging.wanderlust.com
Database: PostgreSQL 15
Cache: Redis
Admin: [Provided separately]
Used For: Final regression testing, performance validation
```

---

## 🧬 Test Data Setup

### Predefined Test Users

#### Admin Account
```
Username: testadmin
Email: admin@example.com
Password: AdminPass123!
Permissions: All
```

#### Regular Test Users
```
User 1:
- Username: john_traveler
- Email: john@example.com
- Password: TravelPass123!
- Bookings: 2

User 2:
- Username: jane_explorer
- Email: jane@example.com
- Password: ExplorePass123!
- Bookings: 0

User 3:
- Username: mike_adventure
- Email: mike@example.com
- Password: AdventurePass123!
- Bookings: 1
```

### Sample Destinations
```
1. Paris, France - Romantic getaway
2. Tokyo, Japan - Cultural experience
3. New York, USA - Urban adventure
4. Bali, Indonesia - Beach paradise
5. Barcelona, Spain - Architecture & culture
6. Sydney, Australia - Natural wonders
```

### Sample Tour Packages
```
Easy Packages (4):
- Paris City Tour (5 days, $899)
- Tokyo Cherry Blossoms (4 days, $949)
- Bali Beach Retreat (6 days, $599)
- Sydney Highlights (5 days, $749)

Moderate Packages (4):
- Spain Heritage Tour (10 days, $1,299)
- Japan Full Experience (10 days, $1,599)
- Australia Adventure (12 days, $1,799)
- Indonesia Explorer (8 days, $999)

Challenging Packages (4):
- Himalayan Trek (14 days, $1,899)
- Safari Adventure (10 days, $2,199)
- Patagonia Expedition (12 days, $2,399)
- Arctic Exploration (15 days, $2,899)
```

---

## ✅ Pre-Testing Final Checklist

### Network & Connectivity (5 minutes)
- [ ] Internet connection stable
- [ ] Can ping external sites
- [ ] VPN connected (if required)
- [ ] Firewall allows localhost traffic

### Server & Database (10 minutes)
- [ ] Django server running without errors
- [ ] Database connection established
- [ ] Sample data fully loaded
- [ ] Admin panel accessible

### Tools & Software (10 minutes)
- [ ] Postman installed and collections imported
- [ ] Browser DevTools working
- [ ] JMeter installed (for performance team)
- [ ] Git configured

### Test Data (5 minutes)
- [ ] Test users created and verified
- [ ] Sample destinations available
- [ ] Sample packages displayed
- [ ] Can manual login with test account

### Documentation (5 minutes)
- [ ] Test case templates available
- [ ] Test tracking spreadsheet ready
- [ ] Defect template downloaded
- [ ] Team contact list updated

### Environment Variables (5 minutes)
- [ ] .env file configured
- [ ] DEBUG=True for development
- [ ] Database pointing to local SQLite
- [ ] Email backend set to console

---

## 🚀 Quick Start Commands

### Set Up Everything at Once (Automated Script)

#### Windows (setup.bat)
```batch
@echo off
echo Setting up Wanderlust QA Testing Environment...

REM Clone repository if not exists
if not exist "wanderlust-tours" (
    git clone https://github.com/[your-org]/wanderlust-tours.git
    cd wanderlust-tours
) else (
    cd wanderlust-tours
)

REM Create virtual environment
python -m venv venv
call venv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt

REM Apply migrations
python manage.py migrate

REM Create superuser
echo Creating admin account...
python manage.py shell < setup_admin.py

REM Load sample data
python manage.py create_sample_data

REM Create .env file
copy .env.example .env

echo.
echo ✅ Setup Complete!
echo.
echo Next Steps:
echo 1. Edit .env file with your settings
echo 2. Run: python manage.py runserver
echo 3. Open: http://localhost:8000
echo.
pause
```

#### Mac/Linux (setup.sh)
```bash
#!/bin/bash
set -e

echo "Setting up Wanderlust QA Testing Environment..."

# Clone repository if not exists
if [ ! -d "wanderlust-tours" ]; then
    git clone https://github.com/[your-org]/wanderlust-tours.git
    cd wanderlust-tours
else
    cd wanderlust-tours
fi

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create superuser
echo "Creating admin account..."
python manage.py shell < setup_admin.py

# Load sample data
python manage.py create_sample_data

# Create .env file
cp .env.example .env

echo ""
echo "✅ Setup Complete!"
echo ""
echo "Next Steps:"
echo "1. Edit .env file with your settings"
echo "2. Run: python manage.py runserver"
echo "3. Open: http://localhost:8000"
echo ""
```

---

## 🆘 Troubleshooting Common Issues

### Issue 1: Port 8000 Already in Use
```bash
# Find process using port 8000
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Mac/Linux

# Kill the process
taskkill /PID [PID] /F        # Windows
kill -9 [PID]                 # Mac/Linux

# Or use different port
python manage.py runserver 8001
```

### Issue 2: Database Migration Errors
```bash
# Reset database (DEVELOPMENT ONLY)
python manage.py migrate travel zero
python manage.py migrate

# Or delete SQLite and remigrate
rm db.sqlite3
python manage.py migrate
```

### Issue 3: Static Files Not Loading
```bash
# Collect static files
python manage.py collectstatic --noinput

# For development (should be automatic)
# Check STATIC_URL and STATIC_ROOT in settings.py
```

### Issue 4: Postman Collection Import Fails
```
Solution:
1. Check file format is valid JSON
2. Use "Import as Raw Text" option
3. Or manually create requests
4. Verify URL format is correct
```

### Issue 5: Sample Data Not Loading
```bash
# Check if command exists
python manage.py help create_sample_data

# Load manually if needed
python manage.py shell < seed_data.py

# Or verify management command file exists
ls travel/management/commands/create_sample_data.py
```

### Issue 6: Permission Denied (Mac/Linux)
```bash
# Make scripts executable
chmod +x setup.sh
chmod +x manage.py

# Run with python prefix
python manage.py migrate
```

---

## 🎯 Success Criteria Checklist

By the end of setup, verify:

- [ ] Django server runs without errors
- [ ] Homepage loads at http://localhost:8000
- [ ] Can login to admin panel
- [ ] Database contains sample data
- [ ] 6 destinations visible
- [ ] 12 tour packages visible
- [ ] Postman collection imported
- [ ] Can execute API requests
- [ ] Browser DevTools working
- [ ] JMeter installed (if applicable)
- [ ] All team members have working environment
- [ ] Documentation accessible

---

## 📞 Support & Escalation

### If Setup Fails

**Step 1**: Check requirements
- [ ] Python 3.11+ installed
- [ ] Git installed
- [ ] 500MB+ free disk space
- [ ] Internet connection working

**Step 2**: Check logs
```bash
# View Django logs
python manage.py runserver  # Shows output

# Check error details
python manage.py check      # System check
```

**Step 3**: Escalate
- Ask QA Lead
- Check documentation
- Contact development team
- Check README.md for known issues

---

**Environment Setup Complete! Ready for Testing! 🚀**

Questions? Check the Troubleshooting section above or ask QA Lead.

---

**Document Version**: 1.0  
**Last Updated**: March 30, 2026  
**Owner**: QA Lead
