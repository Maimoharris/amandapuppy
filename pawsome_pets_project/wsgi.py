"""
WSGI config for pawsome_pets_project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pawsome_pets_project.settings')

application = get_wsgi_application()
