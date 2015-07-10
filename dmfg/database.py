from flask_sqlalchemy import SQLAlchemy
from . import app
import os

app.config.from_object(os.environ['APP_SETTINGS'])

db = SQLAlchemy(app)
