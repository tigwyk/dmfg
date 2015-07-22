from dmfg.database import db
import datetime
import humanize
from . import admin


class Item(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    created_date = db.Column(db.DateTime)
    trades = db.relationship("Trade", backref="item")
    mfg_jobs = db.relationship("ManufactureJob", backref="item")

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

class Trade(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime)
    quantity = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))

    def __init__(self, name=""):
        self.name = name
        self.created_date = datetime.datetime.now() 

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

    def __init__(self, name=""):
        self.name = name
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
    items_owned = db.Column(db.String())

    def __init__(self, name="",email="",items_owned={}):
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

    def get_items_owned(self):
        return self.items_owned.items()

    def add_item(self, item_id, qty):
        if item_id in self.items_owned:
            self.items_owned[item_id] = self.items_owned[item_id] + qty
        else:
            self.items_owned[item_id] = qty
        
    def remove_item(self, item_id, qty):
        if (item_id in self.items_owned) and ((self.items_owned[item_id]-qty)>0):
            self.items_owned[item_id] = self.items_owned[item_id] - qty

    @property
    def human_date(self):
        return humanize.naturaldate(self.created_date)

    @property
    def human_time(self):
        return humanize.naturaltime(datetime.datetime.now()-self.created_date)

admin.register(User, session=db.session)
admin.register(Item, session=db.session)
admin.register(Trade, session=db.session)
admin.register(ManufactureJob, session=db.session)
