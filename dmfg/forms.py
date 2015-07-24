###
### Forms
###
###

from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField, validators, TextAreaField, IntegerField
from wtforms.validators import Required
from wtforms.ext.sqlalchemy.orm import model_form
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from .models import Trade,User,Item

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

def item_list():
    return Item.query.all()

def user_list():
    return User.query.all()

class CreateTradeForm(Form):
    quantity = IntegerField('Quantity', [validators.Required()] )
    price = IntegerField('Price', [validators.Required()] )
    order_type = TextField('Order Type', [validators.Required()])
    item = QuerySelectField(query_factory=item_list, get_label='name', allow_blank=False)

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
