from dmfg.database import db
import datetime
import humanize
from . import admin


class Item(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    created_date = db.Column(db.DateTime)
    trades = db.relationship("Trade", backref="item")

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
    mfg_jobs = db.relationship("ManufactureJob", backref="creator")

    def __init__(self, name="",email=""):
        self.name = name
        self.created_date = datetime.datetime.now()
        self.email = email

    def __repr__(self):
        return '<id %r name=%r>' % (self.id, self.name)

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def get_id(self):
        return unicode(str(self.id))

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
