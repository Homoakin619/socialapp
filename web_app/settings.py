"""
Django settings for web_app project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path

import dj_database_url
import environ
import os

env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = env('SECRET_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')


# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False
DEBUG = True
ALLOWED_HOSTS = ['*']

MAIL_API_KEY = os.environ.get('MAIL_API_KEY')

CSRF_TRUSTED_ORIGINS = [
    'https://socialapp.up.railway.app',
    'http://localhost:8000',
]

# SECURE_SSL_REDIRECT = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

LOGIN_URL = 'account_login'
LOGIN_REDIRECT_URL = 'home'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # My Apps
    'core',
    'chat',
    'channels',
    'cloudinary_storage',
    'cloudinary',
    'authentication',
    'allauth',
    'allauth.account',
    'allauth.socialaccount'
]


SITE_ID = 1
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_FORMS = {'signup':'authentication.forms.UserRegistrationForm'}


AUTHENTICATION_BACKEND = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'web_app.urls'

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


REDIS_URL = os.environ.get('REDIS_URL')

# WSGI_APPLICATION = 'web_app.wsgi.application'
ASGI_APPLICATION = 'web_app.asgi.application'

CHANNEL_LAYERS = {
    'default':{
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG':{
            'hosts': [('localhost',6379)]
        }
    }
}


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / "sent_emails"
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'testsite_app'
EMAIL_HOST_PASSWORD = 'mys3cr3tp4ssw0rd'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'Majmaul Uloom Team <noreply@uloom.com>'

DATABASE_URL = os.environ.get('DATABASE_URL')
DATABASES = {
    "default": dj_database_url.config(default=DATABASE_URL, conn_max_age=1800),
}

CHANNEL_LAYERS = {
    'default':{
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG':{
            'hosts': [REDIS_URL,]
        }
    }
}


if not DEBUG:
    DATABASE_URL = os.environ.get('DATABASE_URL')
    DATABASES = {
        "default": dj_database_url.config(default=DATABASE_URL, conn_max_age=1800),
    }

    CHANNEL_LAYERS = {
        'default':{
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG':{
                'hosts': [REDIS_URL,]
            }
        }
    }

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.environ.get('EMAIL_HOST')
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True

    LOGGING = {
            'version': 1,
            'disable_existing_loggers': True,
            'formatters': {
                'verbose': {
                    'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
                    'datefmt' : "%d/%b/%Y %H:%M:%S"
                },
                'simple': {
                    'format': '%(levelname)s %(message)s'
                },
            },
            'handlers': {
                'file': {
                    'level': 'DEBUG',
                    'class': 'logging.FileHandler',
                    # 'filters': ['require_debug_false'],
                    'filename': 'mysite.log',
                    'formatter': 'verbose'
                },
            },
            'loggers': {
                'django': {
                    'handlers':['file'],
                    'propagate': True,
                    'level':'DEBUG',
                },
                'MYAPP': {
                    'handlers': ['file'],
                    'level': 'DEBUG',
                },
            }
        }

    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': os.environ.get('CLOUD_NAME'),
        'API_KEY': os.environ.get('API_KEY'),
        'API_SECRET': os.environ.get('API_SECRET'),
    }


    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'




# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/


STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')
MEDIA_ROOT =  os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
