# 🔐 School Management System

A secure, production-ready school management system built with **Django 5.1 + DRF** backend and **Next.js 16 (React 19)** frontend.

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
│   Next.js 16    │ ◄────────────────────► │   Django 5.1 + DRF      │
│   Frontend      │    withCredentials     │   Backend               │
│   (Port 3000)   │                        │   (Port 8000)           │
├─────────────────┤                        ├─────────────────────────┤
│ • App Router    │                        │ • JWT Authentication    │
│ • Admin & Public│                        │ • SimpleJWT             │
│ • Zustand 5     │                        │ • Token Blacklist       │
│ • Tailwind v4   │                        │ • Custom AdminUser      │
│ • Framer Motion │                        │ • PostgreSQL Database   │
└─────────────────┘                        └─────────────────────────┘
```

## 📁 Project Structure

```
.
├── backend/                    # Django Backend
│   ├── apps/                   # Django Apps (academics, admissions, authentication, communication, core, gallery, landing, school_info)
│   ├── config/                 # Django project settings
│   │   ├── settings.py         # Main configuration
│   │   └── urls.py             # Root URL routing
│   ├── requirements.txt        # Backend dependencies
│   ├── .env                    # Environment variables
│   └── Dockerfile              # Setup for containerization
│
└── frontend-school/            # Frontend Directory
    └── frontend/               # Next.js 16 Frontend
        ├── src/
        │   ├── app/            # App Router (Admin & Public)
        │   ├── components/     # Reusable Components
        │   ├── lib/            # API & Types
        │   └── stores/         # Zustand Stores
        ├── package.json        # Frontend dependencies
        └── .env.local          # Frontend env variables
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
   # (Optional) Create default admin if your custom command exists:
   # python manage.py createdefaultadmin
   python manage.py runserver
   ```
   Backend will run at: `http://localhost:8000`

### Frontend Setup (Next.js)

1. **Install & Run**:
   ```bash
   cd frontend-school/frontend
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

### Backend (`backend/.env`)
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

### Frontend (`frontend-school/frontend/.env.local`)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🚢 Deployment

The project is structured with a containerized **Django Backend** (typically secured behind a Cloudflare Tunnel) and a **Next.js Frontend** which can be deployed to standard Node.js hosting providers like Vercel.

### Deploying the Backend (Docker & Cloudflare)

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
Open `.env` and fill in your secrets, including Django settings, Database credentials, R2 credentials, and your **Cloudflare Tunnel Token** (`TUNNEL_TOKEN`).

#### 3. Update Nginx Server Name
Open `nginx/default.conf` and update `server_name` to match your domain:
```nginx
server_name your-backend-api-domain.com localhost;
```

#### 4. Spin up the Containers
```bash
docker compose up -d
```
This runs PostgreSQL (`db`), Django (`backend`), Nginx (`nginx`), and Cloudflare Tunnel (`tunnel`).

#### 5. Collect Static Files & Setup DB
```bash
docker compose exec backend python manage.py collectstatic --noinput
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py createsuperuser
```

#### 6. Set Up Hostname Routing in Cloudflare
Go to your **Cloudflare Zero Trust Dashboard** -> **Tunnels**:
1. Select your Tunnel and go to **Public Hostnames**.
2. Add a hostname (e.g., `your-backend-api-domain.com`).
3. Set the service type to **`HTTP`** and URL to **`nginx:80`** (using internal Docker service routing).

### Deploying the Frontend (Vercel Recommended)

1. Push your code to your GitHub repository.
2. Log in to [Vercel](https://vercel.com) and click **Add New Project**.
3. Import your repository, and ensure the **Root Directory** is set to `frontend-school/frontend`.
4. In the **Environment Variables** section, add the following key-value pairs:
   * `NEXT_PUBLIC_API_URL` = `https://your-backend-api-domain.com`
   * `NEXT_PUBLIC_R2_URL` = `https://your-media-r2-domain.com`
   * `NEXT_PUBLIC_APP_URL` = `https://your-frontend-domain.com`
5. Click **Deploy**. Vercel will build and serve your Next.js application automatically with built-in SSL.
