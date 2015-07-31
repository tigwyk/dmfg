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
from .database import db

admin = Admin(app,index_view=models.MyAdminIndexView())

#admin.register(models.User, session=db.session)
admin.register(models.Item, session=db.session)
admin.register(models.Trade, session=db.session)
admin.register(models.Factory, session=db.session)
admin.register(models.Distributor, session=db.session)
admin.register(models.ManufactureJob, session=db.session)
admin.add_view(MyModelView(models.User, db.session))

celery = tasks.make_celery(app)
