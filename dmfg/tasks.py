from celery import Celery
import os

queue = Celery('tasks', broker=os.environ['BROKER_URL'])
