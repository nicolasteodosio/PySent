# -*- coding: utf-8 -*-
from celery import Celery
from datetime import timedelta

BROKER_URL = 'redis://localhost:6379/0'

celery = Celery('EOD_TASKS', broker=BROKER_URL)

# Loads settings for Backend to store results of tweets
celery.config_from_object("celeryconfig")

CELERY_RESULT_BACKEND = 'redis'
CELERY_IMPORTS = ("fetcher.api",)

CELERYBEAT_SCHEDULE = {
    'every-20-seconds': {
        'task': 'fetcher.api.search',
        'schedule': timedelta(seconds=20),
        'args': ['#superbowl'],
    },
}