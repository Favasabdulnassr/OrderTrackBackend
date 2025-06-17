import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OrderTrack.settings')

app = Celery('OrderTrack')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Configure Celery Beat
app.conf.beat_schedule = {
    'process-warehouse-emails': {
        'task': 'order.tasks.process_warehouse_confirmation_emails',
        'schedule': 60.0,  # Run every 60 seconds
    },
}

app.conf.timezone = 'UTC'


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')