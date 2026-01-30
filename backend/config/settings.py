"""
Django settings for School Admin Authentication System.
"""

import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from project root
load_dotenv(BASE_DIR.parent / '.env')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')

# Trust Nginx to handle SSL
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Application definition
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    # Core app
    'apps.core',
    'apps.authentication',
    'storages', # Django Storages for R2/S3
    # New Architecture Apps
    # 'apps.core', # Conflict with existing 'core' app
    'apps.landing',
    'apps.school_info',
    'apps.admissions',
    'apps.academics',
    'apps.communication',
    'apps.gallery',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.gzip.GZipMiddleware',  # Optimized for 1GB Server: Compresses responses
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# Using PostgreSQL
# Intelligent Host Resolution: Fallback to localhost if 'db' (Docker) is unreachable
postgres_host = os.getenv('POSTGRES_HOST', '127.0.0.1')
if postgres_host == 'db':
    try:
        import socket
        socket.gethostbyname('db')
    except (socket.gaierror, ImportError):
        postgres_host = '127.0.0.1'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'school_db'),
        'USER': os.getenv('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', ''),
        'HOST': postgres_host,
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
}

# Caching - Optimized for 1GB RAM (No Redis)
# uses the DB instead of RAM for shared state
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'site_cache_table',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Custom User Model
AUTH_USER_MODEL = 'authentication.AdminUser'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# R2 Custom Domain (includes https:// at start)
R2_CUSTOM_DOMAIN = os.getenv('R2_CUSTOM_DOMAIN', '')
# Remove https:// for django-storages if it exists
CLEAN_R2_DOMAIN = R2_CUSTOM_DOMAIN.replace('https://', '').replace('http://', '')

# Static files (CSS, JavaScript, Images)
STATIC_URL = f'{R2_CUSTOM_DOMAIN}/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (Uploads)
MEDIA_URL = f'{R2_CUSTOM_DOMAIN}/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# R2 Storage Settings
AWS_ACCESS_KEY_ID = os.getenv('R2_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('R2_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('R2_BUCKET_NAME')
AWS_S3_ENDPOINT_URL = os.getenv('R2_ENDPOINT_URL')
AWS_S3_CUSTOM_DOMAIN = CLEAN_R2_DOMAIN
AWS_S3_REGION_NAME = 'auto'
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = True

STORAGES = {
    "default": {
        "BACKEND": "config.storages.R2MediaStorage",
    },
    "staticfiles": {
        "BACKEND": "config.storages.R2StaticStorage",
    }
}



# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'EXCEPTION_HANDLER': 'apps.authentication.utils.custom_exception_handler',
    
    # Throttling (Rate Limiting)
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '5000/day',     # Reduced strictness for public visitors (was 100/day)
        'user': '20000/day',    # Generous limit for admins
        'burst': '100/min',     # Protection against DOS bursts
    },
}

# Simple JWT Configuration - Increased for stability
ACCESS_TOKEN_LIFETIME = int(os.getenv('ACCESS_TOKEN_LIFETIME_MINUTES', 60))
REFRESH_TOKEN_LIFETIME = int(os.getenv('REFRESH_TOKEN_LIFETIME_DAYS', 7))

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=ACCESS_TOKEN_LIFETIME),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=REFRESH_TOKEN_LIFETIME),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': True,
    
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

# CORS Configuration
CORS_ALLOWED_ORIGINS = os.getenv(
    'CORS_ALLOWED_ORIGINS', 
).split(',')

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]


# CSRF Settings (Required for HTTPS Admin/Login)
CSRF_TRUSTED_ORIGINS = os.getenv(
    'CSRF_TRUSTED_ORIGINS',
    'http://localhost:3000,http://127.0.0.1:3000'
).split(',')
CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SAMESITE = 'None' if not DEBUG else 'Lax'
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SAMESITE = 'Lax'

# Logging Configuration
# Explicitly configured to log to Console (stdout).
# Docker/Droplet will capture this. To prevent storage drain,
# ensure Docker Log Rotation is configured on the server.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',  # Only log Warnings/Errors by default to save space
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',  # Log Django info (like startup/requests)
            'propagate': False,
        },
        'content': {  # Your app
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
