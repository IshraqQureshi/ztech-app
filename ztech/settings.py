import os

APP_NAME = 'ZTech Security'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'x@=k5=lfh)-o%0jj5pm#bjizzvvu2h_cf0&21+bw#og%k#gwmo'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'apps.authentication',
    'apps.appcontrol.dashboard',
    'apps.appcontrol.users',
    'apps.appcontrol.userroles',
    'apps.appcontrol.user_profile',
    'ztech',    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 'ztech.middleware.UserRoleAuthentication',
]

ROOT_URLCONF = 'ztech.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR + '/templates/'],
        'APP_DIRS': True,
        'OPTIONS': {
             'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'ztech.context_processors.static_root',
                'ztech.context_processors.settings_constants',
            ],
        },
    },
]

WSGI_APPLICATION = 'ztech.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

ADMIN_EMAIL = 'info@ztech.com'

# SMTP DETAILS
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mailtrap.io'
EMAIL_USE_TLS = False
EMAIL_PORT = 25
EMAIL_HOST_USER = '6a9938dce2ec0a'
EMAIL_HOST_PASSWORD = 'ba0ab894eea17b'


STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")    
]

# General Static files (CSS, JavaScript, Images)
GENERAL_STATIC_URL = '/static/general/'
GENERAL_STATIC_ROOT = os.path.join(BASE_DIR, '/static/general/')

# Appcontrol Static files (CSS, JavaScript, Images)
APPCONTROL_STATIC_URL = '/static/appcontrol/'
APPCONTROL_STATIC_ROOT = os.path.join(BASE_DIR, '/static/appcontrol/')

# Frontend Static files (CSS, JavaScript, Images)
FRONTEND_STATIC_URL = '/static/frontend/'
FRONTEND_STATIC_ROOT = os.path.join(BASE_DIR, '/static/frontend/')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
