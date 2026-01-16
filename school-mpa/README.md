# Django School Website MPA

A pure Django multi-page application for school websites. Migrated from Next.js + Django REST API.

## Quick Start

### 1. Create Virtual Environment
```bash
cd school-mpa
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Environment
Copy the existing `.env` from parent directory or create one:
```bash
cp ../.env .env
```

Required variables:
- `SECRET_KEY` - Django secret key
- `DEBUG` - True/False
- `POSTGRES_HOST`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`

### 4. Create Cache Table
```bash
python manage.py createcachetable
```

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Create Admin User
```bash
python manage.py createsuperuser
```

### 7. Run Development Server
```bash
python manage.py runserver
```

Visit: http://localhost:8000

## Project Structure

```
school-mpa/
├── config/          # Django settings, URLs, WSGI
├── core/            # Base models, utilities, context processors
├── content/         # Content models (30+ models for all sections)
├── authentication/  # Admin user model, session auth
├── public_site/     # Public page views and URLs
├── admin_panel/     # Admin dashboard and CRUD views
├── templates/
│   ├── base.html
│   ├── partials/    # Header, footer
│   ├── public/      # Public page templates
│   └── admin/       # Admin panel templates
├── static/          # CSS, JS, images
└── media/           # Uploaded files
```

## Features

- **Public Pages**: Home, About, Academics, Admissions, Contact, Facilities, Gallery, Notices, Events, Public Disclosure
- **Admin Panel**: Dashboard, Site Settings, Notices, Events, Contact Submissions
- **Session-based Auth**: Replaces JWT with Django sessions
- **TailwindCSS**: Via CDN for simplicity
- **S3/CloudFront**: Optional media storage

## Deployment

For production:
```bash
DEBUG=False python manage.py collectstatic
gunicorn config.wsgi:application
```
