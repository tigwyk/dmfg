from celery import Celery

queue = Celery('tasks', broker=dmfg.config['CELERY_BROKER_URL'])
