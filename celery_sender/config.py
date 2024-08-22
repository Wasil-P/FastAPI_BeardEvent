import os
from celery import Celery
from dotenv import load_dotenv
from celery.schedules import crontab
import celery_sender.tasks

load_dotenv()


def make_celery():
    celery = Celery(
        'worker',
        backend=f"redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}/0",
        broker=f"redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}/0"
    )
    celery.conf.update(
        beat_schedule={
            'add-every-30-seconds': {
                'task': 'celery_sender.tasks.event_reminder',
                'schedule': crontab(hour="8", minute="0")
            },
        },
        timezone='UTC',
    )

    return celery


celery = make_celery()

