# Production Deployment Guide (Django Backend)

This guide details the steps to deploy the Django Backend to a DigitalOcean Droplet using Docker, Nginx, and Let's Encrypt SSL.

## 1. Prerequisites
- **DigitalOcean Droplet** (Ubuntu 22.04 or later).
- **Domain Name** (e.g., `api.yourschool.com`) pointing to the Droplet's IP via an **A Record**.
- **SSH Access** to the server.

---

## 2. Server Setup (First Time)

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
