from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^+3s)n@s!d2fdsqm=v-1oc*y+ekr8zs3!*pn6-fzk!j5^6)k0h'


# Local Database
DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "ebdb",
        "USER": "postgres",
        "PASSWORD": "admin",
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
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# MEDIA_URL = '/media/'


# Media files (AWS)
AWS_STORAGE_BUCKET_NAME = 'lyka-seller-center-dev'
AWS_ACCESS_KEY_ID = 'AKIAYO6GTQEHMJXJRD3Y'
AWS_SECRET_ACCESS_KEY = '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'
AWS_S3_CUSTOM_DOMAIN = 'dhor4ba6a2l1k.cloudfront.net'
AWS_S3_FILE_OVERWRITE = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = "https://dhor4ba6a2l1k.cloudfront.net/"
MEDIAFILES_LOCATION = os.environ.get('MEDIAFILES_LOCATION')
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

try:
    from .local import *
except ImportError:
    pass
