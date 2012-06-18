import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),'settleup')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settleup.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
