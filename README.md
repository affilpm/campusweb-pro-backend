# 🔐 School Management System (Test Phase)

A secure, production-ready school management system built with **Django + DRF** backend and **Next.js** frontend.

> [!WARNING]
> **TEST PHASE**: The frontend and backend are currently split into separate repositories for testing a major refactor. Please follow the "Repositories & Branches" section below closely.

## 📋 Table of Contents

- [Repositories & Branches](#repositories--branches-test-phase)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Authentication Flow](#authentication-flow)
- [Security Features](#security-features)
- [Deployment (Critical Info)](#deployment-cicd-critical)

## 🕸 Repositories & Branches (Test Phase)

The project is currently split into two separate repositories.

| Component | Repository | Active Branch |
|-----------|------------|---------------|
| **Backend** | `affilpm/school` | `new-test-phase-code-refactored-backend-and-frontend-changed` |
| **Frontend** | `affilpm/school-frontend` | `new-test-phase-code-refactored-backend-and-frontend-changed` |

**Note**: The backend deployment is currently set to `[skip ci]` to prevent crashing the production database until a manual reset is performed.

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

*Note: In the current Test Phase, these are in separate repositories.*

```
.
├── backend/                    # Django Backend (In `school` repo)
│   ├── apps/                   # Django Apps (academics, authentication, core, etc.)
│   ├── config/                 # Django project settings
│   │   ├── settings.py         # Main configuration
│   │   └── urls.py             # Root URL routing
│   ├── .env                    # Environment variables
│   └── Dockerfile              # Setup for containerization
│
└── frontend/                   # Next.js Frontend (In `school-frontend` repo)
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

1. **Clone the backend repo and switch branch**:
   ```bash
   git clone https://github.com/affilpm/school.git backend-repo
   cd backend-repo
   git checkout new-test-phase-code-refactored-backend-and-frontend-changed
   ```

2. **Setup Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install django djangorestframework djangorestframework-simplejwt django-cors-headers psycopg2-binary python-dotenv
   pip install -r requirements.txt
   ```

3. **Run Migrations & Server**:
   ```bash
   # WARNING: This will set up the new database structure
   python manage.py migrate
   python manage.py createdefaultadmin
   python manage.py runserver
   ```
   Backend will run at: `http://localhost:8000`

### Frontend Setup (Next.js)

1. **Clone the frontend repo and switch branch**:
   ```bash
   git clone https://github.com/affilpm/school-frontend.git frontend-repo
   cd frontend-repo
   git checkout new-test-phase-code-refactored-backend-and-frontend-changed
   ```

2. **Install & Run**:
   ```bash
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

## � API Reference

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
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgres://...
CORS_ALLOWED_ORIGINS=http://localhost:3000
ACCESS_TOKEN_LIFETIME_MINUTES=15
REFRESH_TOKEN_LIFETIME_DAYS=7
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🚢 Deployment (CI/CD) & Critical Refactor Info

The project uses a **Hybrid Deployment Strategy** automation via **GitHub Actions** and **Docker Hub**.

### Automated Workflow
1.  **Push to `main`**: Triggers `.github/workflows/deploy.yml`.
2.  **Build**: GitHub builds the Docker image and pushes it to [Docker Hub](https://hub.docker.com/r/affil/school-backend).
3.  **Deploy**: GitHub connects to your DigitalOcean droplet via SSH and runs:
    ```bash
    git pull origin main       # Updates config (docker-compose.yml)
    docker compose pull backend # Downloads new app code
    docker compose up -d       # Restarts containers
    ```

### ⚠️ CRITICAL: Database Refactor & First Deployment
**This Test Phase includes a complete database refactor.** Standard migration strategies will **FAIL** because the migration history has been broken/reset.

**For the first deployment of this phase, you MUST reset the production database:**

1. **SSH into the server**:
   ```bash
   ssh root@your-server-ip
   ```

2. **Stop and Wipe**:
   ```bash
   cd ~/school
   docker compose down
   # CAUTION: This deletes all data
   docker volume rm school_postgres_data
   ```

3. **Pull & Start**:
   ```bash
   git pull origin new-test-phase-code-refactored-backend-and-frontend-changed
   # Ensure docker-compose.yml pulls the correct image tag if changed
   docker compose up -d --build
   ```

## 📄 License

MIT License
