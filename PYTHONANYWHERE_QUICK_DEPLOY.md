# Deploy to PythonAnywhere (Free Tier) - Quick Checklist

Time Required: 20-30 minutes
Status: Ready for this project

---

## 1) Create PythonAnywhere Account

1. Sign up at https://www.pythonanywhere.com
2. Choose a free Beginner account
3. Open Dashboard

---

## 2) Open a Bash Console and Upload Project

If your code is already on GitHub:

```bash
git clone <YOUR_GITHUB_REPO_URL> ~/tours_project
cd ~/tours_project
```

If your code is local only, upload zip from Files tab, then extract:

```bash
cd ~
unzip tours_project.zip
cd tours_project
```

---

## 3) Create Virtual Environment and Install Dependencies

```bash
mkvirtualenv --python=/usr/bin/python3.10 toursenv
workon toursenv
cd ~/tours_project
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

---

## 4) Create Environment File

Create `~/tours_project/.env` with values below:

```env
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=replace_with_long_random_secret
ALLOWED_HOSTS=dhanush1348.pythonanywhere.com,localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=https://dhanush1348.pythonanywhere.com
GOOGLE_API_KEY=your_google_api_key
```

Production mode is now safe on PythonAnywhere:
- If `DATABASE_URL` is not set, the project falls back to SQLite.
- If `REDIS_URL` is not set, the project falls back to local memory cache.

---

## 5) Run Django Setup Commands

```bash
workon toursenv
cd ~/tours_project
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### One-Command Option

Instead of running the setup commands one by one, use the deploy helper script:

```bash
cd ~/tours_project
chmod +x scripts/pythonanywhere_deploy.sh
./scripts/pythonanywhere_deploy.sh
```

If your virtualenv does not exist yet, run:

```bash
cd ~/tours_project
chmod +x scripts/pythonanywhere_deploy.sh
./scripts/pythonanywhere_deploy.sh --bootstrap-venv
```

Script options:

```bash
./scripts/pythonanywhere_deploy.sh --help
```

---

## 6) Configure Web App in PythonAnywhere

1. Go to Web tab
2. Click Add a new web app
3. Choose Manual configuration
4. Choose Python 3.10

Set these fields:
- Source code: `/home/dhanush1348/tours_project`
- Working directory: `/home/dhanush1348/tours_project`
- Virtualenv: `/home/dhanush1348/.virtualenvs/toursenv`

---

## 7) Update WSGI Configuration

In Web tab, open WSGI config file and replace content with:

```python
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

path = '/home/dhanush1348/tours_project'
if path not in sys.path:
    sys.path.insert(0, path)

# Load environment variables from project .env
load_dotenv(Path(path) / '.env')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tours_project.settings')

# Optional: hard-pin production mode in case .env is missing
os.environ.setdefault('ENVIRONMENT', 'production')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Save the file.

---

## 8) Configure Static and Media Files

In Web tab, add static mappings:
- URL: `/static/`  Directory: `/home/dhanush1348/tours_project/staticfiles`
- URL: `/media/`   Directory: `/home/dhanush1348/tours_project/media`

Before first reload, ensure the static directory exists:

```bash
cd ~/tours_project
workon toursenv
python manage.py collectstatic --noinput
```

---

## 9) Reload and Test

1. Click Reload in Web tab
2. Open: `https://dhanush1348.pythonanywhere.com`
3. Test home page, package listing, and booking flow

Admin URL:
- `https://dhanush1348.pythonanywhere.com/admin/`

---

## Quick Troubleshooting

See error log:
- Web tab -> Error log

Common fixes:
1. Module not found: activate correct virtualenv and run `pip install -r requirements.txt` again.
2. DisallowedHost: add domain to `ALLOWED_HOSTS` in `.env`, then reload app.
3. Static files missing: run `python manage.py collectstatic --noinput` and verify static mapping path.
4. App not loading after edits: click Reload in Web tab.

---

## Notes for This Repository

- Your Django settings already support `.env` loading.
- Your static settings already use `STATIC_ROOT = BASE_DIR / 'staticfiles'`.
- No code changes are required for a basic PythonAnywhere free deployment.
