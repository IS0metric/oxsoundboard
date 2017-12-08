"""
WSGI config for oxsoundboard project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import sys
import db_conf
from django.core.wsgi import get_wsgi_application

path = db_conf.WS_PATH
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "oxsoundboard.settings")

application = get_wsgi_application()
