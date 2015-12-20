# -*- coding: utf-8 -*-
from celery import Celery
from celery.schedules import crontab

BROKER_URL = 'redis://localhost:6379/0'

celery = Celery('EOD_TASKS', broker=BROKER_URL)

# Loads settings for Backend to store results of tweets
celery.config_from_object("celeryconfig")

CELERY_RESULT_BACKEND = 'redis'
CELERY_IMPORTS = ("fetcher.api",)

CELERYBEAT_SCHEDULE = {
    'every-minute': {
        'task': 'fetcher.api.search',
        'schedule': crontab(),
        'args': ['#Esquenta'],
    },
}