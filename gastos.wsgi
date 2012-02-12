import os
import sys

print sys.path

sys.path.append('/home/bruno/Projects')
sys.path.append('/home/bruno/Projects/gastos')

os.environ['DJANGO_SETTINGS_MODULE'] = 'gastos.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
