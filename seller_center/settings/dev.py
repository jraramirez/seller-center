from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^+3s)n@s!d2fdsqm=v-1oc*y+ekr8zs3!*pn6-fzk!j5^6)k0h'


# Local Database
DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "seller_center",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "localhost",
        "PORT": "",
    }
}


# Static files (Local)
STATICFILES_LOCATION = 'static'
STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'


# Media files (Local)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

try:
    from .local import *
except ImportError:
    pass
