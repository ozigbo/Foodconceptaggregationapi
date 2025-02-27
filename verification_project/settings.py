"""
Django settings for verification_project project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
from pathlib import Path
import environ
import os




# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Construct the absolute path to the .env_settings file
env_file_path = BASE_DIR / '.env_settings'

# Initialize the environ.Env object
env = environ.Env()

# Read environment variables from the .env_settings file
env.read_env(env_file_path)

#env = environ.Env.read_env(env_file_path)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-$kj9uypm-by)j*v#57sw4t@gwm_zwd3n4(zg^kji3s!(osfm(1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['900e-2603-7081-63b-c78-4de3-b4bc-dc05-426d.ngrok-free.app','localhost']

CORS_ALLOW_ALL_ORIGINS = True  # Allow requests from any origin (not recommended for production)


# Application definition

INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'verification_backendapp',
    'celery',
    'drf_yasg',
    'rest_framework',
    'rest_framework_simplejwt'

]


# settings.py

MSAL_CLIENT_ID = env('MSALCLIENTID')
MSAL_CLIENT_SECRET = env('MSALCLIENTSECRET')
MSAL_REDIRECT_URI = 'https://localhost:5173'  # Make sure this matches the redirect URI configured in Azure AD
MSAL_AUTHORITY = env('MSALAUTHORITY')
MS_TOKEN_URL=env('MS_TOKEN_URL')


MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    #"django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = 'verification_project.urls'

#CORS_ORIGIN_ALLOW_ALL = True



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

REFRESH_TOKEN_EXP = 24
ACCESS_TOKEN_EXP = 1

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=ACCESS_TOKEN_EXP),
    'REFRESH_TOKEN_LIFETIME': timedelta(hours=REFRESH_TOKEN_EXP),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY[::-1],
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'TOKEN_TYPE_CLAIM': 'token_type',
    'token_blacklist': {
        'gc_interval': 3600,  # set to an hour.
    },
}



AUTH_USER_MODEL = 'verification_backendapp.User' 



REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # ... other authentication classes
    ),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    
    # ... other settings
}

# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,  # Number of items per page
}


SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "api_key": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header"
        },
    },
    #"LOGIN_URL": "rest_framework:login",
    #"LOGOUT_URL": "rest_framework:logout",
    "USE_SESSION_AUTH": False,
}

REST_USE_JWT = True

JWT_COOKIE_NAME = 'login'

WSGI_APPLICATION = 'verification_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases




# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': env('DATABASE'),
        'USER': env('USERNAME'),
        'PASSWORD': env('PASSWORD'),
        'HOST': env('HOST'),   # Or an IP Address that your DB is hosted on
        'PORT': env('PORT'),
    }
    
}


REFRESH_TOKEN_EXP = 24
ACCESS_TOKEN_EXP = 1

# settings.py

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

CELERY_REDIRECT_STDOUTS = True
CELERY_REDIRECT_STDERRS = True

# settings.py
CELERY_TASK_ALWAYS_EAGER = True  # Run tasks synchronously for testing and development

# settings.py

CELERY_BEAT_SCHEDULE = {
    'my_task': {
        'task': 'verification_backendapp.tasks.my_task',
        'schedule': 5.0,  # Every 10 seconds
    },
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
