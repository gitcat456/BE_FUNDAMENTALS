from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_#tpqm-0=ktj1julxjmpa5um927wa1*qpff_#*zk10&2sscv%n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "denz.tests"]


# Application definition

INSTALLED_APPS = [
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

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
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

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
]

ROOT_URLCONF = 'config.urls'

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


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

INTERNAL_IPS = ['127.0.0.1']

# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'


REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    )
}

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


from decouple import config

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

                                

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django.db.backends": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
}
