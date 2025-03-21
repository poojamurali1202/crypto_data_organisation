from __future__ import absolute_import,unicode_literals
from celery import Celery
from django.conf import settings
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project',broker='redis://localhost:6379/0')
app.conf.enable_utc = False
app.conf.update(timezone='Asia/kolkata')

# Celery Beat Settings
app.conf.beat_schedule = {

}
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request:{self.request!r}')
