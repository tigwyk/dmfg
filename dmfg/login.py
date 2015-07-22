from flask.ext.login import LoginManager
from . import app
from .models import User

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)