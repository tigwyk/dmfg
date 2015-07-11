from celery import Celery

queue = Celery('tasks', broker=BROKER_URL)
