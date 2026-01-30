# Production Deployment Guide (Django Backend)

This guide details the steps to deploy the Django Backend to a DigitalOcean Droplet using Docker, Nginx, and Let's Encrypt SSL.

## 1. Prerequisites
- **DigitalOcean Droplet** (Ubuntu 22.04 or later).
- **Domain Name** (e.g., `api.yourschool.com`) pointing to the Droplet's IP via an **A Record**.
- **SSH Access** to the server.

---

---
---

## 2. Server Setup (First Time)

### ⚠️ Critical Performance Tuning: Add Swap Memory
**Important:** 1GB Droplets will likely crash without Swap memory when running Docker. Run these commands to create a 2GB swap file:

```bash
# Check if swap exists
sudo swapon --show

# If empty, create swap file
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Make it permanent
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### Install Docker & Docker Compose
Connect to your server via SSH:
```bash
ssh root@<DROPLET_IP>
```

Run these commands to install Docker:
```bash
sudo apt update
sudo apt install docker.io docker-compose-plugin -y
```

### Clone the Repository
```bash
git clone https://github.com/affilpm/school.git
cd school
```

---

## 3. Configuration

### Environment Variables (.env)
Create the `.env` file on the server:
```bash
nano .env
```

Paste the production configuration (ensure you update secrets):

```bash
# Security
SECRET_KEY=change-this-to-a-secure-random-string
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,<DROPLET_IP>,api.yourschool.com

# Database (Internal Docker Networking)
POSTGRES_DB=school_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_db_password
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Cloudflare R2 (Static & Media Files)
USE_R2=True
R2_ACCESS_KEY_ID=your_key_id
R2_SECRET_ACCESS_KEY=your_secret_key
R2_BUCKET_NAME=school-media-assets
R2_ENDPOINT_URL=https://<account_id>.r2.cloudflarestorage.com
R2_CUSTOM_DOMAIN=pub-<id>.r2.dev

# CORS (Frontend Access)
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://yourschool.com
```

### Configure Nginx for HTTPS
1. Ensure `docker-compose.yml` exposes port 443 and maps certificates:
   ```yaml
   nginx:
     ports:
       - "80:80"
       - "443:443"
     volumes:
       - ./nginx/default.conf:/etc/nginx/conf.d/default.conf:ro
       - /etc/letsencrypt:/etc/letsencrypt:ro
   ```

---

## 4. SSL Certificates (Certbot)

**Run this ONCE to generate certificates:**

1. Stop Nginx to free up port 80:
   ```bash
   docker compose stop nginx
   ```
2. Run Certbot (Standalone mode):
   ```bash
   sudo apt install certbot -y
   sudo certbot certonly --standalone -d api.yourschool.com
   ```
   *Follow the prompts. Certificates will be saved to `/etc/letsencrypt/live/api.yourschool.com/`.*

3. Update `nginx/default.conf` to use the certificates:
   ```nginx
   server {
       listen 80;
       server_name api.yourschool.com;
       return 301 https://$host$request_uri;
   }

   server {
       listen 443 ssl;
       server_name api.yourschool.com;

       ssl_certificate /etc/letsencrypt/live/api.yourschool.com/fullchain.pem;
       ssl_certificate_key /etc/letsencrypt/live/api.yourschool.com/privkey.pem;

       location / {
           proxy_pass http://backend:8000;
           proxy_set_header Host $host;
           # ... standard headers ...
       }
   }
   ```

---

## 5. Deployment Commands

### Build and Start
```bash
docker compose up -d --build
```

### Initial Data Setup (Run Once)
```bash
# 1. Migrate Database
docker compose exec backend python manage.py migrate

# 2. Create Cache Table (Required for performance)
docker compose exec backend python manage.py createcachetable

# 3. Create Superuser (For Admin Access)
docker compose exec backend python manage.py createsuperuser

# 4. Fill Dummy Data (Optional, for fresh sites)
docker compose exec backend python manage.py fill_dummy_data

# 5. Populate SEO Data (Recommended)
docker compose exec backend python populate_seo.py
```

---

## 6. Maintenance & Updates

### Updating Code
To deploy new changes from GitHub:
```bash
# 1. Pull changes
git pull origin main

# 2. Rebuild containers (if requirements or code changed)
docker compose up -d --build --force-recreate

# 3. Apply migrations (if models changed)
docker compose exec backend python manage.py migrate
```

### Troubleshooting
- **500 Server Error**: Check logs: `docker compose logs -f backend`
- **Connection Refused**: Check if Nginx is running: `docker compose ps`
- **Database Connection Error**: Ensure `POSTGRES_HOST=db` in `.env`.

---

## 7. Destructive Updates & Data Restoration

**⚠️ WARNING: Use this ONLY if you have refactored models and need to reset the database.**

### Pre-requisites
1. **Local Backup**: Ensure you have `backend/db_backup_full_YYYYMMDD_HHMMSS.json` on your local machine.
2. **Transfer Backup**: Upload the backup to the server.
   ```bash
   # Run this from your LOCAL machine
   scp backend/db_backup_full_YYYYMMDD_HHMMSS.json root@<DROPLET_IP>:/root/school/backend/backup.json
   ```

### Reset & Restore Procedure
Connect to your server and run these commands:

1. **Pull Latest Code**
   ```bash
   cd school
   git pull origin main
   ```

2. **Rebuild Containers**
   ```bash
   docker compose up -d --build --force-recreate
   ```

3. **Reset Database (Wipes ALL Data)**
   ```bash
   docker compose exec backend python manage.py flush --no-input
   ```

4. **Apply New Schema**
   ```bash
   docker compose exec backend python manage.py migrate
   ```

5. **Restore Data**
   ```bash
   docker compose exec backend python manage.py loaddata backup.json
   ```

6. **Verify**
   Check if the site is running and data is present.
