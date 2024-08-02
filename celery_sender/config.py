from celery import Celery


def make_celery():
    celery = Celery(
        'worker',
        backend='redis://localhost:6379/0',
        broker='redis://localhost:6379/0'
    )
    celery.conf.update(
        result_expires=3600,
        beat_schedule={
            'add-every-30-seconds': {
                'task': 'app.tasks.add',
                'schedule': 30.0,
                'args': (16, 16)
            },
        },
        timezone='UTC',
    )
    return celery

celery = make_celery()