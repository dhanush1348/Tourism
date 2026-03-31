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
ENVIRONMENT=development
DEBUG=False
SECRET_KEY=replace_with_long_random_secret
ALLOWED_HOSTS=<your-username>.pythonanywhere.com,localhost,127.0.0.1
GOOGLE_API_KEY=your_google_api_key
```

Why `ENVIRONMENT=development` here:
- Your current settings use PostgreSQL only when ENVIRONMENT=production.
- On free PythonAnywhere, SQLite is the easiest path and works with your current project.

---

## 5) Run Django Setup Commands

```bash
workon toursenv
cd ~/tours_project
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

---

## 6) Configure Web App in PythonAnywhere

1. Go to Web tab
2. Click Add a new web app
3. Choose Manual configuration
4. Choose Python 3.10

Set these fields:
- Source code: `/home/<your-username>/tours_project`
- Working directory: `/home/<your-username>/tours_project`
- Virtualenv: `/home/<your-username>/.virtualenvs/toursenv`

---

## 7) Update WSGI Configuration

In Web tab, open WSGI config file and replace content with:

```python
import os
import sys

path = '/home/<your-username>/tours_project'
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tours_project.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Save the file.

---

## 8) Configure Static and Media Files

In Web tab, add static mappings:
- URL: `/static/`  Directory: `/home/<your-username>/tours_project/staticfiles`
- URL: `/media/`   Directory: `/home/<your-username>/tours_project/media`

---

## 9) Reload and Test

1. Click Reload in Web tab
2. Open: `https://<your-username>.pythonanywhere.com`
3. Test home page, package listing, and booking flow

Admin URL:
- `https://<your-username>.pythonanywhere.com/admin/`

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
