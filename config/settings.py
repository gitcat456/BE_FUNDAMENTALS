from pathlib import Path
import dj_database_url
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost').split(',')


# Application definition

INSTALLED_APPS = [
    'payments',
    'posts',
    'coredata',
    'ecom',
    'revamp',
    'lib',
    'debug_toolbar',
    'corsheaders',
    'rest_framework',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
]

AUTH_USER_MODEL = 'lib.User'
ROOT_URLCONF = 'config.urls'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'posts.middleware.RequestLoggerMiddleware',
    'lib.middleware.RequestLoggerMiddleware',
]

# ── CORS ─────────────────────────────────────────────
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:5173'
).split(',')




TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'config.wsgi.application'


DATABASE_URL = config('DATABASE_URL', default=None)

if DATABASE_URL:
    # production → PostgreSQL from Railway
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,  # keep connections alive 10 mins
        )
    }
else:
    # local development → SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

INTERNAL_IPS = ['127.0.0.1']


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
}


# REST_FRAMEWORK = {
#     'DEFAULT_RENDERER_CLASSES': (
#         'rest_framework.renderers.JSONRenderer',
#         'rest_framework.renderers.BrowsableAPIRenderer',
#     )
# }

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'lib.jwt_authentication.JWTAuthentication',
        'lib.api_key_auth.APIKeyAuthentication',  #api-key token authentication
        'lib.authentication.TokenAuthentication',  # Your custom token auth
        'rest_framework.authentication.SessionAuthentication',  # Keep session for browsable API
    ],
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticated',
    # ],
}

# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'lib.validators.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'lib.validators.UppercaseValidator',
    },
    {
        'NAME': 'lib.validators.LowercaseValidator',
    },
    {
        'NAME': 'lib.validators.NumberValidator',
    },
    {
        'NAME': 'lib.validators.SpecialCharacterValidator',
    },
]

#                     Your Django App
                        #     ↓
                        # Reads .env via decouple
                        #     ↓
                        # Connects to SMTP server
                        #     ↓
                        # Authenticates
                        #     ↓
                        # Sends email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  #protocol to sed email
EMAIL_HOST = config('EMAIL_HOST')          #mail server adress to connect to 
EMAIL_PORT = config('EMAIL_PORT', cast=int)  #communication channel 587-TLS 465-SSL
EMAIL_HOST_USER = config('EMAIL_HOST_USER')    #username to authenticate to the mail server 
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')  #password/apikey to log in to the server 
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)    #TLS to encrypt the connection
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')   #default sender adress

FRONTEND_URL = config('FRONTEND_URL', default='http://localhost:5173')


# ── SECURITY HEADERS (production only) ───────────────
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000         # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# ── LOGGING ──────────────────────────────────────────
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO'
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False
        },
        'payments': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}


import cloudinary

cloudinary.config(
    cloud_name=config('CLOUDINARY_CLOUD_NAME'),
    api_key=config('CLOUDINARY_API_KEY'),
    api_secret=config('CLOUDINARY_API_SECRET'),
    secure=True  # always use https
)

MAPBOX_ACCESS_TOKEN = config('MAPBOX_ACCESS_TOKEN')

GOOGLE_CLIENT_ID = config('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = config('GOOGLE_CLIENT_SECRET')


# config/settings.py
TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = config('TWILIO_PHONE_NUMBER')
TWILIO_WHATSAPP_NUMBER = config('TWILIO_WHATSAPP_NUMBER')

#paystak configurations
PAYSTACK_SECRET_KEY = config('PAYSTACK_SECRET_KEY')
PAYSTACK_PUBLIC_KEY = config('PAYSTACK_PUBLIC_KEY')
LOAN_PRICE_KES = 50
PAYSTACK_CALLBACK_URL = config('PAYSTACK_CALLBACK_URL')

# ── STORAGE CONFIGURATION ────────────────────────────
# django-storages handles all S3/MinIO communication.
# When you swap to AWS S3 in production:
# → change AWS_S3_ENDPOINT_URL to None (uses AWS default)
# → update credentials in .env
# → zero code changes anywhere else
# ─────────────────────────────────────────────────────

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_ENDPOINT_URL = config('AWS_S3_ENDPOINT_URL', default=None) or None 
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='us-east-1')


# AT
AT_USERNAME = config('AT_USERNAME', default='sandbox')
AT_API_KEY = config('AT_API_KEY', default='')
AT_SENDER_ID = config('AT_SENDER_ID', default='')

# don't append auth querystring to every URL
AWS_QUERYSTRING_AUTH = False

# cache control — browser caches files for 1 day
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

# ── STORAGES (Django 4.2+ way) ───────────────────────
STORAGES = {
    # static files → still served locally (CSS, JS)
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
    # media files → go to MinIO/S3
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
}

# where media files are accessible
MEDIA_URL = f"{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/"
