import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()


def make_celery():
    celery_sender = Celery(
        'worker',
        backend=f"redis://{os.getenv('HOST')}:{os.getenv('REDIS_PORT')}/0",
        broker=f"redis://{os.getenv('HOST')}:{os.getenv('REDIS_PORT')}/0"
    )
    celery_sender.conf.update(
        beat_schedule={
            'add-every-30-seconds': {
                'reminder': 'celery_sender.tasks.event_reminder',
                'schedule': 30.0
            },
        },
        timezone='UTC',
    )
    return celery_sender


celery_sender = make_celery()
