# 🔐 School Management System - Backend

A secure, production-ready backend for the School Management System, built with **Django 5.1 + DRF**.

> Note: This repository contains only the Backend API code. The frontend Next.js application is maintained in a separate repository.

## 📋 Table of Contents

- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Authentication Flow](#authentication-flow)
- [Security Features](#security-features)
- [Deployment (Docker & Cloudflare)](#deployment-docker--cloudflare)

## 🏗 Architecture

The backend provides a RESTful API powered by Django REST Framework (DRF). It manages authentication, the PostgreSQL database, and media storage via Cloudflare R2.

```
┌─────────────────────────────────────────────────────────────────────┐
│                         SYSTEM ARCHITECTURE                         │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────┐       HTTP/REST        ┌─────────────────────────┐
│   Next.js 16    │ ◄────────────────────► │   Django 5.1 + DRF      │
│  (Separate Repo)│    withCredentials     │   Backend (This Repo)   │
├─────────────────┤                        ├─────────────────────────┤
│ • App Router    │                        │ • JWT Authentication    │
│ • Zustand 5     │                        │ • SimpleJWT             │
│ • Tailwind v4   │                        │ • Token Blacklist       │
│                 │                        │ • Custom AdminUser      │
│                 │                        │ • PostgreSQL Database   │
└─────────────────┘                        └─────────────────────────┘
```

## 📁 Project Structure

```
.
└── backend/                    # Django Backend Application
    ├── apps/                   # Django Apps (academics, admissions, authentication, communication, core, gallery, landing, school_info)
    ├── config/                 # Django project settings
    │   ├── settings.py         # Main configuration
    │   └── urls.py             # Root URL routing
    ├── requirements.txt        # Backend dependencies
    ├── .env                    # Environment variables
    └── Dockerfile              # Setup for containerization
```

## 🚀 Getting Started

### Local Setup

1. **Setup Environment**:
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Run Migrations & Server**:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```
   The backend API will run at: `http://localhost:8000`

### Default Admin Credentials (if seeded)

| Email | Password |
|-------|----------|
| `admin@school.edu` | `<your_password>` |

## 📖 API Reference

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/admin/auth/login/` | Login admin user |
| POST | `/api/admin/auth/logout/` | Logout (blacklist token) |
| POST | `/api/admin/auth/refresh/` | Refresh access token |
| GET | `/api/admin/auth/me/` | Get current user |
| POST | `/api/admin/auth/verify/` | Verify access token |

## 🔄 Authentication Flow

Authentication uses HttpOnly cookies for the refresh token and JSON body responses for the short-lived access token, providing strong protection against XSS and CSRF.

1. **Login**: Client sends `{ email, password }` to `/api/admin/auth/login/`.
2. **Response**: Backend sets a `refresh_token` in a Secure HttpOnly cookie, and returns the `access` token in the JSON body.
3. **Refresh**: When the access token expires, the client calls `/api/admin/auth/refresh/`. The backend reads the `refresh_token` cookie and issues a new access token.

## 🔒 Security Features

### Token Security
| Feature | Implementation |
|---------|---------------|
| Token Algorithm | HS256 |
| Access Token Expiry | 15 minutes |
| Refresh Token Expiry | 7 days |
| Token Blacklist | Enabled (logout invalidation) |

### Cookie Configuration
```python
REFRESH_TOKEN_COOKIE_HTTPONLY = True    # Prevents XSS
REFRESH_TOKEN_COOKIE_SECURE = True      # HTTPS only (production)
REFRESH_TOKEN_COOKIE_SAMESITE = 'Lax'   # CSRF protection
```

## 📝 Environment Variables

Create a `.env` file inside the `backend` directory based on `.env.example`:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,your-backend-api-domain.com
DATABASE_URL=postgres://...
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://your-backend-api-domain.com
ACCESS_TOKEN_LIFETIME_MINUTES=15
REFRESH_TOKEN_LIFETIME_DAYS=7

# Cloudflare R2 Settings
R2_ACCESS_KEY_ID=your-r2-access-key-id
R2_SECRET_ACCESS_KEY=your-r2-secret-access-key
R2_BUCKET_NAME=your-bucket-name
R2_ENDPOINT_URL=https://<account-id>.r2.cloudflarestorage.com
R2_CUSTOM_DOMAIN=https://your-media-r2-domain.com

# Cloudflare Tunnel Configuration
TUNNEL_TOKEN=your-cloudflare-tunnel-token
```

## 🚢 Deployment (Docker & Cloudflare)

The backend is fully containerized using **Docker** and secured behind a **Cloudflare Tunnel** with **Nginx** acting as a reverse proxy. This setup isolates the host ports from the public internet.

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/affilpm/campusweb-pro-backend.git
   cd campusweb-pro-backend
   ```

2. **Configure Environment Variables**:
   Copy `.env.example` to `.env` and fill in your secrets, database credentials, R2 credentials, and your **Cloudflare Tunnel Token** (`TUNNEL_TOKEN`).

3. **Update Nginx Server Name**:
   Open `nginx/default.conf` and update `server_name` to match your domain:
   ```nginx
   server_name your-backend-api-domain.com localhost;
   ```

4. **Spin up the Containers**:
   ```bash
   docker compose up -d
   ```
   This runs PostgreSQL (`db`), Django (`backend`), Nginx (`nginx`), and Cloudflare Tunnel (`tunnel`).

5. **Collect Static Files & Setup DB**:
   ```bash
   docker compose exec backend python manage.py collectstatic --noinput
   docker compose exec backend python manage.py migrate
   docker compose exec backend python manage.py createsuperuser
   ```

6. **Set Up Hostname Routing in Cloudflare**:
   Go to your **Cloudflare Zero Trust Dashboard** -> **Tunnels**:
   * Select your Tunnel and go to **Public Hostnames**.
   * Add a hostname (e.g., `your-backend-api-domain.com`).
   * Set the service type to **`HTTP`** and URL to **`nginx:80`** (using internal Docker service routing).
