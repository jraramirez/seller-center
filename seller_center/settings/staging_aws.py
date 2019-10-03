from .base import *

DEBUG = True
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
ALLOWED_HOSTS = ['seller-center-staging.ap-southeast-1.elasticbeanstalk.com']


# Database
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

#This is where you put your CLOUDFRONT URL ex: 'd3rdlm5j4gpnnq.cloudfront.net'
AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_S3_CUSTOM_DOMAIN')
AWS_S3_FILE_OVERWRITE = True


STATIC_ROOT = '/static/'
#url for static files ex: "https://d3rdlm5j4gpnnq.cloudfront.net/"
STATIC_URL = os.environ.get('STATIC_URL')

# Static files (AWS)
STATICFILES_LOCATION = os.environ.get('STATICFILES_LOCATION')
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]

# Media files (Local)
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# MEDIA_URL = '/media/'

AWS_AUTH_URL = os.environ.get('AWS_AUTH_URL')

AUTHENTICATION_BACKENDS = [
                            'base.aws_backend.AwsBackend',
                            'django.contrib.auth.backends.ModelBackend'
                          ]

# Media files (AWS)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
#Media url ex: "https://d3rdlm5j4gpnnq.cloudfront.net/"
MEDIA_URL = os.environ.get('MEDIA_URL')
MEDIAFILES_LOCATION = os.environ.get('MEDIAFILES_LOCATION')
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


try:
    from .local import *
except ImportError:
    pass
