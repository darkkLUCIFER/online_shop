import os

from celery import Celery
from datetime import timedelta

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

celery_app = Celery('config')

# Load task modules from all registered Django apps.
celery_app.autodiscover_tasks()

celery_app.conf.broker_url = "amqp://"
celery_app.conf.result_backend = "rpc://"
celery_app.conf.task_serializer = "json"
celery_app.conf.result_serializer = "pickle"
celery_app.conf.accept_content = ['pickle', 'json']
celery_app.conf.result_expires = timedelta(days=1)

# block client to do a task or not
celery_app.conf.task_always_eager = False

# how many task can do each worker if tasks are heavy set to 1 and if easy tasks set to 4
celery_app.conf.worker_prefetch_multiplier = 4
