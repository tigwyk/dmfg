import os
from flask import Flask
from flask_bootstrap import Bootstrap
import logging, sys
from flask_superadmin import Admin

logging.basicConfig(stream=sys.stderr)
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

app = Flask(__name__,template_folder=tmpl_dir)
admin = Admin(app)
Bootstrap(app)

from . import views
from . import login
from . import models
from . import tasks
from . import auth
from . import forms

celery = tasks.make_celery(app)
