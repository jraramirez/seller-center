from .base import *

DEBUG = True
SECRET_KEY = 'tuIPxdVIRqVrLbOgOXnbeZ6MBVXBgngJa'
ALLOWED_HOSTS = ['seller-center-dev.vpsbnhp5gf.ap-southeast-1.elasticbeanstalk.com'] 


# Database
print(os.environ)
if 'RDS_HOSTNAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }


# AWS S3 Storage
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_FILE_OVERWRITE = True


# Static files (AWS)
STATICFILES_LOCATION = os.environ.get('STATICFILES_LOCATION')
STATICFILES_STORAGE = 'custom_storages.StaticStorage'
STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]

STATIC_ROOT = '/static/'
STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN

# Media files (Local)
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# MEDIA_URL = '/media/'

AUTHENTICATION_BACKENDS = [
                            'base.aws_backend.AwsBackend'
                            ]

# Media files (AWS)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
MEDIAFILES_LOCATION = os.environ.get('MEDIAFILES_LOCATION')
DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_PASSWORD = 'f0rtune$1'
# EMAIL_HOST_USER = 'mirr@digiters.co'
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


try:
    from .local import *
except ImportError:
    pass
