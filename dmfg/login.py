from flask_googlelogin import GoogleLogin
from dmfg import app
from dmfg.models import User

googlelogin = GoogleLogin(app)

@googlelogin.user_loader
def load_user(userid):
	return User.query.get_or_404(userid)
