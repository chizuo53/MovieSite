import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MovieSite.settings')

app = Celery('proj')

from django.conf import settings

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(settings.INSTALLED_APPS)

