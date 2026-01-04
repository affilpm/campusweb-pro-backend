#!/bin/bash

# Create cache table (fail silently if exists)
python manage.py createcachetable || true

# Run migrations
python manage.py migrate --noinput

# Collect static files (optional)
python manage.py collectstatic --noinput

# Populate initial SEO data (only if missing)
python populate_seo.py

# Start gunicorn
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120 --forwarded-allow-ips "*"
