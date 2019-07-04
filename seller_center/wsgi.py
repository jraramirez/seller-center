"""
WSGI config for seller_center project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seller_center.settings.dev")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seller_center.settings.production")

application = get_wsgi_application()
