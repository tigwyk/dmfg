from dmfg.database import db
from sqlalchemy.dialects.postgresql import JSON
import datetime
import humanize
import json
from . import admin

class Item(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    created_date = db.Column(db.DateTime)
    trades = db.relationship("Trade", backref="item")
    mfg_jobs = db.relationship("ManufactureJob", backref="item")
    distributors = db.relationship("Distributor", backref="product")

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

#class Factory(db.Model):
    
    #id = db.Column(db.Integer, primary_key=True)
    #name = db.Column(db.String())
    #capacity = db.Column(db.Integer)
    #current_job = db.relationship("ManufactureJob", backref="factory")
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    #def __init__(self, name=None, capacity=0, owner=None):
        #self.name = name
        #self.capacity = capacity
        #self.owner = owner

    #def __repr__(self):
        #return '<factory id %r name=%r>' % (self.id, self.name)    

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
    #factory_id = db.Column(db.Integer, db.ForeignKey('factory.id'))

    def __init__(self, name="",quantity=0,user=None,item=None''',factory=None'''):
        self.name = name
        self.quantity = quantity
        self.user = user
        self.item = item
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
    #factories = db.relationship("Factory",backref="owner")
    distributors = db.relationship("Distributor", backref="owner")

    def __init__(self, name="",email="",items_owned=dict()):
        self.name = name
        self.created_date = datetime.datetime.now()
        self.email = email
        self.items_owned = items_owned


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
    
    def get_owned_item(self, item_id):
        if str(item_id) in self.get_items_owned().viewkeys():
            return (item_id, self.get_items_owned().get(str(item_id)))
        else:
            return False

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

admin.register(User, session=db.session)
admin.register(Item, session=db.session)
admin.register(Trade, session=db.session)
#admin.register(Factory, session=db.session)
admin.register(Distributor, session=db.session)
admin.register(ManufactureJob, session=db.session)
