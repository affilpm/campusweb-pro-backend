# 🔐 School Management System

A secure, production-ready school management system built with **Django + DRF** backend and **Next.js** frontend.

## 📋 Table of Contents

- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Authentication Flow](#authentication-flow)
- [Security Features](#security-features)
- [Deployment](#deployment)

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         SYSTEM ARCHITECTURE                         │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────┐       HTTP/REST        ┌─────────────────────────┐
│   Next.js       │ ◄────────────────────► │   Django + DRF          │
│   Frontend      │    withCredentials     │   Backend               │
│   (Port 3000)   │                        │   (Port 8000)           │
├─────────────────┤                        ├─────────────────────────┤
│ • Admin Login   │                        │ • JWT Authentication    │
│ • Dashboard     │                        │ • SimpleJWT             │
│ • Zustand Store │                        │ • Token Blacklist       │
│ • Axios Client  │                        │ • Custom AdminUser      │
└─────────────────┘                        └─────────────────────────┘
```

## 📁 Project Structure

```
.
├── backend/                    # Django Backend
│   ├── apps/                   # Django Apps (academics, authentication, core, etc.)
│   ├── config/                 # Django project settings
│   │   ├── settings.py         # Main configuration
│   │   └── urls.py             # Root URL routing
│   ├── .env                    # Environment variables
│   └── Dockerfile              # Setup for containerization
│
└── frontend/                   # Next.js Frontend
    ├── src/
    │   ├── app/                # App Router (Admin & Public)
    │   ├── components/         # Reusable Components
    │   ├── lib/                # API & Types
    │   └── stores/             # Zustand Stores
    ├── package.json
    └── .env.local              # Frontend env variables
```

## 🚀 Getting Started

### Backend Setup (Django)

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
   python manage.py createdefaultadmin
   python manage.py runserver
   ```
   Backend will run at: `http://localhost:8000`

### Frontend Setup (Next.js)

1. **Install & Run**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   Frontend will run at: `http://localhost:3000`

### Access the Application

- **Frontend**: http://localhost:3000
- **Admin Login**: http://localhost:3000/admin/login
- **Backend API**: http://localhost:8000
- **Django Admin**: http://localhost:8000/django-admin/

### Default Admin Credentials

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

### Login Example

**Request:**
```http
POST /api/admin/auth/login/
Content-Type: application/json

{
  "email": "admin@school.edu",
  "password": "<your_password>"
}
```

**Response:**
```json
{
  "success": true,
  "user": {
    "email": "admin@school.edu",
    "role": "super_admin"
  },
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## 🔄 Authentication Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                        AUTHENTICATION FLOW                          │
└─────────────────────────────────────────────────────────────────────┘

1. USER LOGIN
   ┌──────────┐      POST /api/admin/auth/login/     ┌─────────────────┐
   │  Next.js │ ─────────────────────────────────► │    Django       │
   │  Client  │     { email, password }             │    Backend      │
   └──────────┘                                     └────────┬────────┘
                                                             │
2. TOKEN GENERATION (SimpleJWT)                              │
                                                    ┌────────▼────────┐
                                                    │ RefreshToken.   │
                                                    │   for_user()    │
                                                    └────────┬────────┘
                                                             │
3. RESPONSE                                                  │
   ┌──────────┐  Set-Cookie: refresh_token (HttpOnly) ┌──────▼────────┐
   │  Next.js │ ◄───────────────────────────────────  │    + access   │
   │  Client  │  + access token in JSON body          │    token      │
   └──────────┘                                       └───────────────┘

4. AUTO TOKEN REFRESH (Axios Interceptor)
   ┌──────────┐  401 Response                    ┌─────────────┐
   │  Client  │ ◄──────────────────────────────  │    API      │
   └────┬─────┘                                  └─────────────┘
        │
        ▼
   POST /api/admin/auth/refresh/ (with cookie)
        │
        └───────► New access token ───────► Retry original request
```

## 🔒 Security Features

### Token Security
| Feature | Implementation |
|---------|---------------|
| Access Token Storage | In-memory (Zustand store) |
| Refresh Token Storage | HTTP-only cookie |
| Token Algorithm | HS256 |
| Access Token Expiry | 15 minutes |
| Refresh Token Expiry | 7 days |
| Token Blacklist | Enabled (logout invalidation) |

### Cookie Configuration (Django)
```python
REFRESH_TOKEN_COOKIE_HTTPONLY = True    # Prevents XSS
REFRESH_TOKEN_COOKIE_SECURE = True      # HTTPS only (production)
REFRESH_TOKEN_COOKIE_SAMESITE = 'Lax'   # CSRF protection
```

## 📝 Environment Variables

### Backend (.env)
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

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🚢 Deployment

The project is containerized using **Docker** and secured behind a **Cloudflare Tunnel** with **Nginx** acting as a reverse proxy. This setup isolates the host ports from the public internet, routing all traffic through Cloudflare's secure network.

### How to Deploy from Git (For Others)

To clone and spin up this deployment environment on a new machine:

#### 1. Clone the Repository
```bash
git clone https://github.com/affilpm/campusweb-pro-backend.git
cd campusweb-pro-backend
```

#### 2. Configure Environment Variables
Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```
Open `.env` and fill in your secrets, including:
* Django settings (`SECRET_KEY`, `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`).
* Database credentials (`POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`).
* Cloudflare R2 Credentials (`R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_BUCKET_NAME`, etc.).
* **Cloudflare Tunnel Token** (`TUNNEL_TOKEN`).

#### 3. Update Nginx Server Name
Open `nginx/default.conf` and update `server_name` to match your domain:
```nginx
server_name your-backend-api-domain.com localhost;
```

#### 4. Spin up the Containers
Run Docker Compose in detached mode:
```bash
docker compose up -d
```
This builds/downloads and runs PostgreSQL (`db`), Django (`backend`), Nginx (`nginx`), and Cloudflare Tunnel (`tunnel`).

#### 5. Collect Static Files (R2 Upload)
To copy your Django static files to your Cloudflare R2 bucket:
```bash
docker compose exec backend python manage.py collectstatic --noinput
```

#### 6. Initialize Database and Create Admin
Run database migrations and create a superuser for the admin panel:
```bash
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py createsuperuser
```

#### 7. Set Up Hostname Routing in Cloudflare
Go to your **Cloudflare Zero Trust Dashboard** -> **Tunnels**:
1. Select your Tunnel and go to **Public Hostnames**.
2. Add a hostname (e.g., `your-backend-api-domain.com`).
3. Set the service type to **`HTTP`** and URL to **`nginx:80`** (using internal Docker service routing).


