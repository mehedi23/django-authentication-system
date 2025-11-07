from pathlib import Path
from decouple import config, Csv
from datetime import timedelta
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Email Settings
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)
EMAIL_USE_SSL = config('EMAIL_USE_SSL', default=False, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = "no-reply@example.com"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG',default=False,cast=bool)

# Allow all domains (development purposes)
CORS_ALLOW_ALL_ORIGINS = True

# OR restrict to specific domains (recommended for production)
# CORS_ALLOWED_ORIGINS = [
#     "https://example.com",
#     "https://sub.example.com",
# ]

ALLOWED_HOSTS = []

CUSTOM_APPS = [
    'apps.users',
    'apps.verification',
]

INSTALLED_LIBRARIES = [
    "rest_framework", 
    "drf_spectacular",
    'rest_framework_simplejwt.token_blacklist',
]

# Application definition

INSTALLED_APPS = (
    [
        'jazzmin',
        'corsheaders',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ] 
    + INSTALLED_LIBRARIES
    + CUSTOM_APPS
)

AUTH_USER_MODEL = 'users.User' # app_name.ModelName

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Must be at the top
    'django.middleware.common.CommonMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware', 
    # Custom
    'core.middleware.verify_user_status.VerifyUserStatus',
    
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# Check if production
PRODUCTION = config('PRODUCTION', default=False, cast=bool)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': config('POSTGRES_HOST', default='localhost'),
        'PORT': config('POSTGRES_PORT', default='5432'),
    }
}



# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True 

DATA_UPLOAD_MAX_MEMORY_SIZE = 2 * 1024 * 1024  # 2MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 2 * 1024 * 1024  # 2MB

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

# Static files (CSS, JS, Images)
STATIC_URL = '/static/' 
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),  # project-level static folder
]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")  # for collectstatic in production

# Media files (user-uploaded files)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
   'DEFAULT_PERMISSION_CLASSES': [
       'rest_framework.permissions.IsAuthenticated',
   ],
   'DEFAULT_AUTHENTICATION_CLASSES': [
       'rest_framework_simplejwt.authentication.JWTAuthentication', 
   ], 
    # drf_spectacular for rest_framework
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    
    'AUTH_HEADER_TYPES': ("Bearer",), 
    'USER_ID_FIELD': "username",
    'USER_ID_CLAIM': "username",
    'ROTATE_REFRESH_TOKENS': True, # Issue a new refresh token every time the old one is used
    'BLACKLIST_AFTER_ROTATION': True, # Old refresh token is blacklisted immediately after rotation
}

# settings.py
# Run windows Terminal: celery -A core worker --loglevel=INFO -P solo
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379/1')

# Caching in Redis
CACHES = {
    "default": {
        # "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "BACKEND": "django_redis.cache.RedisCache", 
        'LOCATION': 'redis://redis:6379/1', 
    }
} 
# pip install redis:  is the Python client for Redis. It allows Python to connect to a Redis server.
# pip install django-redis : Django-specific cache backend wrapper. It integrates Redis with Django’s cache system.