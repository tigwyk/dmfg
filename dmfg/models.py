# -*- coding: utf-8 -*-
from .database import db
from sqlalchemy.dialects.postgresql import JSON
from flask.ext.superadmin.contrib import sqlamodel
from flask.ext.login import login_required,login_user,logout_user,current_user
from flask.ext.superadmin import AdminIndexView
import datetime
import humanize
import json

class Item(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    created_date = db.Column(db.DateTime)
    trades = db.relationship("Trade", backref="item",lazy="dynamic")
    mfg_jobs = db.relationship("ManufactureJob", backref="item",lazy="dynamic")
    distributors = db.relationship("Distributor", backref="product", lazy="dynamic")

    def __init__(self, name=""):
        self.name = name
        self.created_date = datetime.datetime.now()

    def __repr__(self):
        return '<item id %r name=%r>' % (self.id, self.name)

    @property
    def human_date(self):
        return humanize.naturaldate(self.created_date)

    @property
    def human_time(self):
        return humanize.naturaltime(datetime.datetime.now()-self.created_date)

class Factory(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    capacity = db.Column(db.Integer)
    current_job = db.relationship("ManufactureJob", backref="factory",lazy="dynamic")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self, name=None, capacity=0, owner=None):
        self.name = name
        self.capacity = capacity
        self.owner = owner
        
    @property
    def producing(self):
        return self.current_job.first().item.name

    def __repr__(self):
        return '<factory id %r name=%r>' % (self.id, self.name)    

class Distributor(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    capacity = db.Column(db.Integer)
    product_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self, name=None, capacity=0, owner=None, product=None):
        self.name = name
        self.capacity = capacity
        self.owner = owner
        self.product = product

    def __repr__(self):
        return '<distributor id %r name=%r>' % (self.id, self.name)    

class Trade(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    order_type = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))

    def __init__(self, quantity=0,price=0,order_type="", user=None, item=None):
        self.quantity = quantity
        self.price = price
        self.order_type = order_type
        self.created_date = datetime.datetime.now()
        self.user = user
        self.item = item

    def __repr__(self):
        return '<trade id %r>' % (self.id)

    @property
    def human_date(self):
        return humanize.naturaldate(self.created_date)

    @property
    def human_time(self):
        return humanize.naturaltime(datetime.datetime.now()-self.created_date)

class ManufactureJob(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime)
    quantity = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    factory_id = db.Column(db.Integer, db.ForeignKey('factory.id'))

    def __init__(self, name="",quantity=0,user=None,item=None,factory=None):
        self.name = name
        self.quantity = quantity
        self.user = user
        self.item = item
        self.factory = factory
        self.created_date = datetime.datetime.now() 

    def __repr__(self):
        return '<mfg id %r>' % (self.id)

    @property
    def human_date(self):
        return humanize.naturaldate(self.created_date)

    @property
    def human_time(self):
        return humanize.naturaltime(datetime.datetime.now()-self.created_date)

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    email = db.Column(db.String())
    created_date = db.Column(db.DateTime)
    trades = db.relationship("Trade", backref="user")
    mfg_jobs = db.relationship("ManufactureJob", backref="user")
    items_owned = db.Column(JSON)
    money = db.Column(db.Float)
    factories = db.relationship("Factory",backref="owner")
    distributors = db.relationship("Distributor", backref="owner")

    def __init__(self, name="",email="",items_owned=dict(),money=0):
        self.name = name
        self.created_date = datetime.datetime.now()
        self.email = email
        self.items_owned = items_owned
        self.money = money


    def __repr__(self):
        return '<user id %r name=%r>' % (self.id, self.name)

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def get_id(self):
        return unicode(str(self.id))
    
    def withdraw_funds(self, amount):
        if amount <= self.money:
            self.money = self.money - amount
            return True
        else:
            return False
        
    def deposit_funds(self, amount):
        self.money = self.money + amount
        return True
    
    def get_owned_item(self, item_id):
        if str(item_id) in self.get_items_owned().viewkeys():
            return (item_id, self.get_items_owned().get(str(item_id)))
        else:
            return False
    
    def get_item_quantity(self, item_id):
        return self.get_items_owned().get(str(item_id))

    def get_items_owned(self):
        return json.loads(self.items_owned)

    def add_item(self, item_id, qty):
        items_dict = self.get_items_owned()
        if str(item_id) in items_dict.viewkeys():
            items_dict[str(item_id)] = items_dict[str(item_id)] + qty
        else:
            items_dict[str(item_id)] = qty
        self.items_owned = items_dict
        db.session.add(self)
        db.session.commit()
        return True
        
    def remove_item(self, item_id, qty):
        items_dict = self.get_items_owned()
        if (str(item_id) in items_dict.viewkeys()) and ((items_dict.get(str(item_id))-qty)>=0):
            items_dict[str(item_id)] = items_dict.get(str(item_id)) - qty
            self.items_owned = items_dict
            db.session.add(self)
            db.session.commit()
            return True
        else:
            return False
        
    @property
    def human_date(self):
        return humanize.naturaldate(self.created_date)

    @property
    def human_time(self):
        return humanize.naturaltime(datetime.datetime.now()-self.created_date)

# Create customized model view class
class MyModelView(sqlamodel.ModelView):
    def is_accessible(self):
        return current_user.is_authenticated()


# Create customized index view class
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated()