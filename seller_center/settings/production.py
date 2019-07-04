from .base import *

DEBUG = True
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
ALLOWED_HOSTS = ['seller-center-staging.herokuapp.com'] 


# Database
DATABASE_URL = os.environ.get('DATABASE_URL')
DATABASES = {}
DATABASES['default'] = dj_database_url.parse(DATABASE_URL, conn_max_age=600)


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

try:
    from .local import *
except ImportError:
    pass
