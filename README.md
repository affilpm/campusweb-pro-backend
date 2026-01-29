# 🔐 School Management System (Test Phase)

A secure, production-ready school management system built with **Django + DRF** backend and **Next.js** frontend.

> [!WARNING]
> **TEST PHASE**: The frontend and backend are currently split into separate repositories for testing a major refactor. Please follow the "Repositories & Branches" section below closely.

## 📋 Table of Contents

- [Repositories & Branches](#repositories--branches)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Deployment (Critical Info)](#deployment-critical-info)

## 🕸 Repositories & Branches

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
│ • Zustand Store │                        │ • Postgres DB           │
│ • Axios Client  │                        │ • Tenant-Aware Models   │
└─────────────────┘                        └─────────────────────────┘
```

## 📁 Project Structure

```
.
├── backend/                    # Django Backend (In `school` repo)
│   ├── apps/                   # Django Apps (academics, core, etc.)
│   ├── config/                 # Settings & Configuration
│   ├── .env                    # Environment variables
│   └── Dockerfile              # Setup for containerization
│
└── frontend/                   # Next.js Frontend (In `school-frontend` repo)
    ├── src/
    │   ├── app/                # App Router (Admin & Public)
    │   ├── components/         # Reusable Components
    │   └── lib/                # API & Types
    └── package.json
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
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run Migrations & Server**:
   ```bash
   # WARNING: This will set up the new database structure
   python manage.py migrate
   python manage.py runserver
   ```

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

## 🚢 Deployment (Critical Info)

### ⚠️ Database Refactor Notice

The database structure has been **completely refactored**. Standard migration strategies will fail.

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

---
**License**: MIT
