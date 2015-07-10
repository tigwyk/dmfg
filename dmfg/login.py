from flask_googlelogin import GoogleLogin
from retrade import app
from retrade.models import User

googlelogin = GoogleLogin(app)

@googlelogin.user_loader
def load_user(userid):
	return User.query.get_or_404(userid)
