"""
Django settings for sispostgrado project.

Generated by 'django-admin startproject' using Django 4.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
from django.contrib import messages
from pathlib import Path
import os
from django.urls import reverse_lazy
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-9q=yimpg2(x&t#%f)3c$z^8&or#fp*kq@%98t^-jghjgjg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
#PORT = '80'
ALLOWED_HOSTS = []

#MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'usuario',
    'postgradoApp',     
    'channels',
    'room',
    'daphne',
    'documento',
    'notify',
    
    'video',
]

MIDDLEWARE = [
  
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    
   
]
CORS_ALLOW_ALL_ORIGINS = True # If this is used then `CORS_ALLOWED_ORIGINS` will not have any effect
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
ROOT_URLCONF = 'sispostgrado.urls'
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'sispostgrado.wsgi.application'
ASGI_APPLICATION = 'sispostgrado.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
        
    }
}
# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': BASE_DIR / 'db.sqlite3',  
#DATABASES = {
#    'default': {
#
#        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'NAME': 'dbpostgrado',
#        'USER':'postgres',
#        'PASSWORD':'ruben',
#        'HOST':'localhost',
#        'DATABASE_PORT':'5432',
#    }
#}

DATABASES = {
    'default': {

        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'dbpostgrado',

    }
}
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
#uso de admin usuario
AUTH_USER_MODEL = 'usuario.Usuario'
# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/La_Paz'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
# Archivos staticos
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
MEDIA_URL='/tesis/'
MEDIA_ROOT=os.path.join(BASE_DIR,'tesis')
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Variables de redirección de LOHIN y LOGOUT
LOGIN_REDIRECT_URL = ('/')
LOGOUT_REDIRECT_URL = ('/')
#SESSION_COOKIE_AGE = 20






EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.office365.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "sistemaseguimientotesismaestria@outlook.com"
EMAIL_HOST_PASSWORD = "asddsaaryuytui"
SERVER_EMAIL = EMAIL_HOST_USER



#correo para el envio de correos electronicos
DEFAULT_FROM_EMAIL = 'sistemaseguimientotesismaestria@outlook.com'

#PASSWORD_RESET_TIMEOUT = 100
#SESSION_COOKIE_AGE = 190 
