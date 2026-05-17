from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-expense-tracker-secret-key-change-in-production'
DEBUG = True
ALLOWED_HOSTS = ['*']
import dj_database_url
import os
from dotenv import load_dotenv
load_dotenv()

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tracker',
]

MIDDLEWARE = [
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
        'DIRS': [BASE_DIR / 'templates'],
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

# ─── MySQL Database ────────────────────────────────────────────────────────────
# Make sure MySQL is running and you have created the database:
#   CREATE DATABASE expense_tracker CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
# Update NAME, USER, PASSWORD below to match your MySQL setup.
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'expense_tracker',      
#         'USER': 'root',                  
#         'PASSWORD': 'Admin@123',     
#         'HOST': 'localhost',
#         'PORT': '3306',
#         'OPTIONS': {
#             'charset': 'utf8mb4',
#             'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
#         },
#     }
# }

DATABASES = {
        "default": dj_database_url.config(
            default=os.getenv("DATABASE_URL"), 
            conn_max_age=600, 
            ssl_require=True 
        )
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
