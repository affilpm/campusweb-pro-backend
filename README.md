# 🔐 School Admin Authentication System

A secure, production-ready admin-only authentication system built with **Django + DRF** backend and **Next.js** frontend.

## 📋 Table of Contents

- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Authentication Flow](#authentication-flow)
- [Security Features](#security-features)

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
sch/
├── backend/                    # Django Backend
│   ├── config/                 # Django project settings
│   │   ├── settings.py         # Main configuration
│   │   ├── urls.py             # Root URL routing
│   │   └── wsgi.py             # WSGI config
│   ├── authentication/         # Auth app
│   │   ├── models.py           # AdminUser model
│   │   ├── serializers.py      # DRF serializers
│   │   ├── views.py            # API views
│   │   ├── permissions.py      # Custom permissions
│   │   ├── utils.py            # Helper functions
│   │   ├── urls.py             # Auth URL patterns
│   │   ├── admin.py            # Django admin config
│   │   └── tests.py            # Unit tests
│   ├── manage.py
│   ├── .env                    # Environment variables
│   └── requirements.txt        # Python dependencies
│
└── frontend/                   # Next.js Frontend
    ├── src/
    │   ├── app/
    │   │   ├── admin/
    │   │   │   ├── layout.tsx           # Admin layout wrapper
    │   │   │   ├── admin-layout-client.tsx  # Client layout with sidebar
    │   │   │   ├── page.tsx             # Dashboard page
    │   │   │   └── login/
    │   │   │       └── page.tsx         # Login page
    │   │   ├── layout.tsx               # Root layout
    │   │   └── page.tsx                 # Public homepage
    │   ├── contexts/
    │   │   └── auth-context.tsx         # Auth React context
    │   ├── lib/
    │   │   ├── api.ts                   # Axios client + interceptors
    │   │   └── types.ts                 # TypeScript types
    │   ├── stores/
    │   │   └── auth-store.ts            # Zustand auth store
    │   └── middleware.ts                # Route protection
    ├── package.json
    └── .env.local                       # Frontend env variables
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm or yarn

### Backend Setup (Django)

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers psycopg2-binary python-dotenv

# Run migrations
python manage.py migrate

# Create default admin user
python manage.py createdefaultadmin

# Start development server
python manage.py runserver
```

### Frontend Setup (Next.js)

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

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

### Login

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
  "message": "Login successful",
  "user": {
    "id": 1,
    "email": "admin@school.edu",
    "first_name": "System",
    "last_name": "Administrator",
    "full_name": "System Administrator",
    "role": "super_admin",
    "is_active": true,
    "date_joined": "2024-01-01T00:00:00Z",
    "last_login": "2024-01-01T12:00:00Z"
  },
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response Headers:**
```
Set-Cookie: refresh_token=...; HttpOnly; Path=/api/admin/auth/; SameSite=Lax
```

### Refresh Token

**Request:**
```http
POST /api/admin/auth/refresh/
Cookie: refresh_token=...
```

**Response:**
```json
{
  "success": true,
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Get Current User

**Request:**
```http
GET /api/admin/auth/me/
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "success": true,
  "user": {
    "id": 1,
    "email": "admin@school.edu",
    "first_name": "System",
    "last_name": "Administrator",
    "full_name": "System Administrator",
    "role": "super_admin"
  }
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
                                                             ▼
                                                    ┌─────────────────┐
                                                    │ Validate creds  │
                                                    │ (check_password)│
                                                    └────────┬────────┘
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
        │
        ▼
   ┌────────────────────────────────────────┐
   │ Store access token in Zustand (memory) │
   │ Refresh token automatically in cookie  │
   └────────────────────────────────────────┘

4. PROTECTED API CALLS
   ┌──────────┐  Authorization: Bearer <access>   ┌─────────────┐
   │  Next.js │ ─────────────────────────────► │  Django API │
   │  Client  │                                 │  (Protected)│
   └──────────┘                                 └─────────────┘

5. AUTO TOKEN REFRESH (Axios Interceptor)
   ┌──────────┐  401 Response                    ┌─────────────┐
   │  Client  │ ◄──────────────────────────────  │    API      │
   └────┬─────┘                                  └─────────────┘
        │
        ▼
   POST /api/admin/auth/refresh/ (with cookie)
        │
        └───────► New access token ───────► Retry original request

6. LOGOUT
   ┌──────────┐  POST /api/admin/auth/logout/    ┌─────────────┐
   │  Client  │ ─────────────────────────────► │  Blacklist  │
   │          │  Cookie: refresh_token          │  + Clear    │
   └──────────┘ ◄─────────────────────────────   └─────────────┘
                  Clear-Cookie: refresh_token
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

### Password Security

- Django's built-in password hashing (PBKDF2 + SHA256)
- Minimum 8 characters enforced
- Common password validation

### CORS Configuration

```python
CORS_ALLOWED_ORIGINS = ['http://localhost:3000']
CORS_ALLOW_CREDENTIALS = True  # Required for cookies
```

## 🧪 Running Tests

```bash
cd backend
source venv/bin/activate
python manage.py test authentication
```

## 📝 Environment Variables

### Backend (.env)

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
CORS_ALLOWED_ORIGINS=http://localhost:3000
ACCESS_TOKEN_LIFETIME_MINUTES=15
REFRESH_TOKEN_LIFETIME_DAYS=7
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```



## 🏭 Production Checklist

- [ ] Change `SECRET_KEY` to a secure random value
- [ ] Set `DEBUG=False`
- [ ] Configure PostgreSQL database
- [ ] Set `REFRESH_TOKEN_COOKIE_SECURE=True`
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Set up HTTPS
- [ ] Add rate limiting
- [ ] Configure production CORS origins

## 🚢 Deployment (CI/CD)

The project uses a **Hybrid Deployment Strategy** automation via **GitHub Actions** and **Docker Hub**.

### Architecture
- **Infrastructure:** Managed via `docker-compose.yml` (Git).
- **Application Code:** Managed via Docker Images (`affil/school-backend:latest`).

### Automated Workflow
1.  **Push to `main`**: Triggers `.github/workflows/deploy.yml`.
2.  **Build**: GitHub builds the Docker image and pushes it to [Docker Hub](https://hub.docker.com/r/affil/school-backend).
3.  **Deploy**: GitHub connects to your DigitalOcean droplet via SSH and runs:
    ```bash
    git pull origin main       # Updates config (docker-compose.yml)
    docker compose pull backend # Downloads new app code
    docker compose up -d       # Restarts containers
    ```

### Server Setup (One-Time)
1.  **SSH Keys**: Ensure `~/.ssh/authorized_keys` on the server contains the GitHub Action's public key.
2.  **Environment**: Create `~/school/.env` manually on the server with production secrets.
3.  **Secrets**: Configure the following Repository Secrets in GitHub:
    - `DOCKER_USERNAME` / `DOCKER_PASSWORD`
    - `SSH_HOST` / `SSH_USER` / `SSH_KEY`

### Manual Deployment (Fallback)
If CI/CD fails, you can deploy manually from your machine:
```bash
# 1. Build and Push
cd backend
docker build --platform linux/amd64 -t affil/school-backend:latest .
docker push affil/school-backend:latest

# 2. Update Server
ssh root@api.affils.site "cd ~/school && docker compose pull && docker compose up -d"
```

## 📄 License

MIT License

