###
### Forms
###
###

from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField, validators, TextAreaField, IntegerField
from wtforms.validators import Required
from wtforms.ext.sqlalchemy.orm import model_form
from .models import Trade

#class LoginForm(Form):
    #email = TextField('Email Address', [validators.Required()])
    #password = PasswordField('Password', [validators.Required()])

    #def __init__(self, *args, **kwargs):
      #Form.__init__(self, *args, **kwargs)
      #self.user = None

    #def validate(self):
      #from main import User
      #rv = Form.validate(self)
      #if not rv:
        #return False

      #user = User.query.filter_by(email=self.email.data).first()
      #if user is None:
        #self.email.errors.append('Unknown email address')
        #return False

      #if not user.check_password(self.password.data):
        #self.password.errors.append('Invalid password')
        #return False

      #self.user = user
      #return True

class CreateTradeForm(Form):
    model_form(Trade, Form)
    #qty = IntegerField('Quantity', [validators.Required()] )
    #body = TextAreaField('Ticket description', [validators.Length(min=10,max=500),validators.Required()] )

#class GiftMoneyForm(Form):
    #recipient = TextField('To', [validators.Length(min=4)])
    #amount = IntegerField('Amount', [validators.Required()])

#class RegistrationForm(Form):
    #realname = TextField('Real name', [validators.Length(min=4, max=25)])
    #nickname = TextField('Nickname', [validators.Length(min=3,max=50)])
    #email = TextField('Email Address', [validators.Length(min=6, max=35)])
    #password = PasswordField('New Password', [
        #validators.Required(),
        #validators.EqualTo('confirm', message='Passwords must match')
    #])
    #confirm = PasswordField('Repeat Password')
    #accept_tos = BooleanField('I accept the TOS', [validators.Required()])
