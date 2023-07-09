import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scalerinstaclone.settings')

BASE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')

app = Celery('scalerinstaclone_celery')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.broker_url = BASE_REDIS_URL
app.conf.beat_scheduler = 'django_celery_beat.schedulers.DatabaseScheduler'

# CELERY COMMANDS:

# For starting celery worker:
# celery -A scalerinstaclone worker -l info -f celery.logs

# For starting celery beat:
# celery -A scalerinstaclone beat -l info -f celery_beat.logs

