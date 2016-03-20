# -*- coding: utf-8 -*-
from celery import Celery
from datetime import timedelta
import os

BROKER_URL = 'redis://localhost:6379/0'

celery = Celery('EOD_TASKS', broker=BROKER_URL)

# Loads settings for Backend to store results of tweets
celery.config_from_object('celeryconfig')

CELERY_RESULT_BACKEND = 'redis'
CELERY_IMPORTS = ("task",)

CELERYBEAT_SCHEDULE = {
    'fetch-tweets': {
        'task': 'task.search',
        'schedule': timedelta(seconds=10),
        'args': [os.environ.get('HASHTAG')],
    },
}