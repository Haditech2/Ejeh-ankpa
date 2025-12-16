"""
ASGI config for Ejeh Ankpa Palace Platform.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ejeh_palace.settings')

application = get_asgi_application()
