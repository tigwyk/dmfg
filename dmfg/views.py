from flask import request, session, g, redirect, url_for, abort, render_template, flash
from flask_login import login_required,login_user,logout_user,current_user
from dmfg import app
from dmfg.models import Trade,User
from dmfg.login import googlelogin
from dmfg.database import db

@app.route('/')
@app.route('/index')
def index():
	gauth_url = googlelogin.login_url(params=dict(next=url_for('profile_page')))
	return render_template('index.html',gauth_login_url=gauth_url)

@app.route('/login')
def login_page():
	return 'Login Page Placeholder'

@app.route('/logout')
def logout_page():
	logout_user()
	return render_template('logged_out.html')

@app.route('/about')
def about_page():
	return render_template('about.html')

@app.route('/help')
def help_page():
	return render_template('help.html')

@app.route('/trade')
@login_required
def trade_page():
	trades = Trade.query.all()
	return render_template('trade.html', my_trades=trades)

@app.route('/mfg')
@login_required
def mfg_page():
	mfg = ManufactureJob.query.all()
	return render_template('mfg.html', my_mfg=mfg)

@app.route('/profile')
@login_required
def profile_page():
	user = current_user
	return render_template('profile.html', user=user)

@app.route('/oauth2callback')
@googlelogin.oauth2callback
def create_or_update_user(token, userinfo, **params):
    user = User.query.filter_by(google_id=userinfo['id']).first()
    if user:
        user.name = userinfo['name']
        #user.avatar = userinfo['picture']
    else:
        user = User(google_id=userinfo['id'],
                    name=userinfo['name']
                    )
    db.session.add(user)
    db.session.flush()
    login_user(user)
    return redirect(url_for('profile_page'))
