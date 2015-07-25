from .models import Trade,User,Item
from .database import db
import random

def create_random_trades():
    for x in random.randrange(2,Item.query.all().count()):
        t = Trade(quantity=random.randrange(5,50), price=random.randrange(50,100), order_type="B", user=User.query.filter_by(name='System').first(), item=Item.query.get(x))
        db.session.add(t)
    db.session.commit()
        