from flask import request, session, g, redirect, url_for, abort, render_template, flash
from flask.ext.login import login_required,login_user,logout_user,current_user
from flask.ext.wtf import Form
from dmfg import app
from dmfg.models import Trade,User,ManufactureJob,Item
from dmfg.database import db
from dmfg.auth import OAuthSignIn
from dmfg.forms import CreateTradeForm,CreateMfgForm

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user is not None and current_user.is_authenticated():
		return redirect(url_for('index'))
	return render_template('login.html',
	                       title='Sign In')

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
	buy_orders = Trade.query.filter_by(order_type="B")
	sell_orders = Trade.query.filter_by(order_type="S")
	my_buy = Trade.query.filter_by(user=current_user,order_type="B")
	my_sell = Trade.query.filter_by(user=current_user,order_type="S")
	return render_template('trade.html', buy_orders=buy_orders,sell_orders=sell_orders, my_buy=my_buy,my_sell=my_sell)

@app.route('/create/trade', methods=['POST', 'GET'])
@login_required
def create_trade_page():
	form = CreateTradeForm(request.form, Trade)
	if form.validate_on_submit():
		trade = Trade(quantity=form.quantity.data, price=form.price.data,item=form.item.data,user=current_user,order_type=form.order_type.data)
		db.session.add(trade)
		db.session.commit()
		flash(u'New trade was successfully submitted!','success')
		return redirect(url_for('trade_page'))
	#flash_errors(form)
	return render_template('create_trade_form.html',form=form)
	
@app.route('/create/mfg', methods=['POST', 'GET'])
@login_required
def create_mfg_page():
	form = CreateMfgForm(request.form, Trade)
	if form.validate_on_submit():
		mfg = ManufactureJob(quantity=form.quantity.data, item=form.item.data,user=current_user)
		db.session.add(mfg)
		db.session.commit()
		flash(u'New manufacture job was successfully submitted!','success')
		return redirect(url_for('mfg_page'))
	#flash_errors(form)
	return render_template('create_mfg_form.html',form=form)

@app.route('/mfg')
@login_required
def mfg_page():
	all_mfg = ManufactureJob.query.all()
	my_mfg = ManufactureJob.query.filter_by(user=current_user)
	return render_template('mfg.html', all_mfg=all_mfg, my_mfg=my_mfg)

@app.route('/profile')
@login_required
def profile_page():
	items_temp = current_user.get_items_owned()
	items_table = []
	for item in items_temp.viewkeys():
		items_table.append([Item.query.get(int(item)),items_temp.get(item),"javascript:void(0);"])
	return render_template('profile.html', items_table=items_table)

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
	# Flask-Login function
	if not current_user.is_anonymous():
		return redirect(url_for('index'))
	oauth = OAuthSignIn.get_provider(provider)
	return oauth.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
	if not current_user.is_anonymous():
		return redirect(url_for('index'))
	oauth = OAuthSignIn.get_provider(provider)
	username, email = oauth.callback()
	if email is None:
		# I need a valid email address for my user identification
		flash('Authentication failed.')
		return redirect(url_for('index'))
	# Look if the user already exists
	user=User.query.filter_by(email=email).first()
	if not user:
		# Create the user. Try and use their name returned by Google,
		# but if it is not set, split the email address at the @.
		nickname = username
		if nickname is None or nickname == "":
			nickname = email.split('@')[0]

		# We can do more work here to ensure a unique nickname, if you 
		# require that.
		user=User(name=nickname, email=email)
		db.session.add(user)
		db.session.commit()
	# Log in the user, by default remembering them for their next visit
	# unless they log out.
	login_user(user, remember=True)
	return redirect(url_for('index'))

def flash_errors(form):
	for field, errors in form.errors.items():
		for error in errors:
			flash(u"Error in the %s field - %s" % (
			        getattr(form, field).label.text,
			        error
			        ),"error")

