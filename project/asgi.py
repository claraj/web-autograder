"""
ASGI entrypoint for asyn server-sent events.
Configures Django an then starts the app defines in ASGI_APPLICATION setting.
"""

import os
import django

from channels.routing import get_default_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

django.setup()

application = get_default_application()
