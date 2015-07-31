# -*- coding: utf-8 -*-
import os
from flask import Flask
from flask_bootstrap import Bootstrap
import logging, sys
from flask.ext.superadmin import Admin

logging.basicConfig(stream=sys.stderr)
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

app = Flask(__name__,template_folder=tmpl_dir)
Bootstrap(app)

from . import views
from . import login
from . import models
from . import tasks
from . import auth
from . import forms
from . import inject_trades

admin = Admin(app,index_view=models.MyAdminIndexView())

celery = tasks.make_celery(app)
