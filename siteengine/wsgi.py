"""
WSGI config for siteengine project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os, sys
path = '/var/www/bethink/siteengine'
if path not in sys.path:
    sys.path.append(path)
sys.path.append('/var/www/bethink/venv')
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'siteengine.settings')

application = get_wsgi_application()
