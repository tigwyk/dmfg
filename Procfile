web: gunicorn dmfg:app --log-file - --debug
celery: python manage.py celeryd -c 3 --beat
