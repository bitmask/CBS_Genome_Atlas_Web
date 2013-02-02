import os
import sys

path = '/home/genome_atlas/genome_atlas'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'genome_atlas.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

