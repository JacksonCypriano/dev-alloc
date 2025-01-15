import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_scheduler = 'celery.beat:PersistentScheduler'
app.conf.beat_schedule_filename = '/home/digifrete/digifrete/celerybeat-schedule'

app.conf.update(
    worker_log_format=settings.LOGGING['formatters']['verbose']['format'],
    worker_redirect_stdouts_level='ERROR',
)

app.conf.worker_hijack_root_logger = False