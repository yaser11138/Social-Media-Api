from config.env import env
from celery.schedules import crontab
# https://docs.celeryproject.org/en/stable/userguide/configuration.html

CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='amqp://guest:guest@localhost//')
CELERY_RESULT_BACKEND = 'django-db'

CELERY_TIMEZONE = 'UTC'

CELERY_TASK_SOFT_TIME_LIMIT = 20  # seconds
CELERY_TASK_TIME_LIMIT = 30  # seconds
CELERY_TASK_MAX_RETRIES = 3

CELERY_BEAT_SCHEDULE = {
    "cleanup-old-notifications": {
    "task": "social_media_api.tasks.tasks.cleanup_old_notifications",
    "schedule": crontab(hour=0, minute=0),  # Run at midnight every day
    },

}