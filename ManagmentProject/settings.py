import os
from datetime import timedelta
from pathlib import Path

from ManagmentProject.env import Settings

BASE_DIR = Path(__file__).resolve().parent.parent

settings = Settings()

SECRET_KEY = settings.django.secret_key
DEBUG = settings.django.debug
ALLOWED_HOSTS = settings.django.allowed_hosts

APPS = (
    'users_app',
)

LIBRARIES = (
    'django_jsonform',
)

INSTALLED_APPS = [
    # 'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    *LIBRARIES,
    *APPS,
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

ROOT_URLCONF = 'ManagmentProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'ManagmentProject.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": settings.db.name,
        "USER": settings.db.user,
        "PASSWORD": settings.db.password,
        "HOST": settings.db.host,
        "PORT": settings.db.port,
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

MEDIA_URL = "/media/"
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = "users_app.User"

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

# Jazzmin
# JAZZMIN_SETTINGS = {
#     "site_title": "Система учета",
#     "site_header": "Барс",
#     "site_footer": "Барс",
#     "site_brand": "Барс",
#     "copyright": "Барс",
#     "site_logo": "ece98517-18ee-4c56-8492-de285f98205a.jpg",
#     "login_logo": "44edbc66-c9a2-4ba3-80cc-f9cd91dcb804.jpg",
#     "login_logo_dark": "44edbc66-c9a2-4ba3-80cc-f9cd91dcb804.jpg",
#     "show_sidebar": True,
#     "hide_apps": ["auth"],
#     "hide_models": ["admin.LogEntry"],
#     "navigation_expanded": True,
# }

