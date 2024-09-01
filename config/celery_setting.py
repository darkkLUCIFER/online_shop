import os

from celery import Celery
from datetime import timedelta

# Set the default Django settings module for the 'celery' program.
# This tells Celery to use the Django settings file for configuration.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Create a new Celery application instance named 'config'.
# This name is typically the same as your Django project name.
celery_app = Celery('config')

# Automatically discover tasks from all registered Django apps.
# This allows Celery to find any tasks.py files in your Django apps and load the tasks.
celery_app.autodiscover_tasks()

# Configuration settings for Celery:

# Define the broker URL that Celery will use to send and receive messages.
# "amqp://" is the default for using RabbitMQ as the message broker.
celery_app.conf.broker_url = "amqp://"

# Define the backend used to store task results.
# "rpc://" means results are sent back as messages (often used with RabbitMQ).
celery_app.conf.result_backend = "rpc://"

# Specify the serialization format for tasks.
# "json" is commonly used because it's human-readable and widely supported.
celery_app.conf.task_serializer = "json"

# Specify the serialization format for storing task results.
# "pickle" is used here because it can handle more complex Python objects than JSON.
celery_app.conf.result_serializer = "pickle"

# List of content types that Celery will accept for task serialization.
# Here, it allows both "pickle" and "json" formats.
celery_app.conf.accept_content = ['pickle', 'json']

# Set the time limit for how long a task result is kept.
# After 1 day (24 hours), the result will expire and be removed from the backend.
celery_app.conf.result_expires = timedelta(days=1)

# Determine whether tasks should be executed locally and immediately.
# Setting this to 'False' means tasks will be sent to the queue and processed asynchronously.
celery_app.conf.task_always_eager = False

# Configure how many tasks a worker can prefetch (take in advance before processing).
# A higher value (e.g., 4) is better for light tasks, while a lower value (e.g., 1) is better for heavy tasks.
celery_app.conf.worker_prefetch_multiplier = 4
