from .models import Trade,User,Item
from .database import db
import random

def create_random_trades():
    x = Item.query.get(random.randrange(2,Item.query.count()+1))
    t = Trade(quantity=random.randrange(5,50), price=random.randrange(50,100), order_type="B", user=User.query.filter_by(name='System').first(), item=x)
    db.session.add(t)
    db.session.commit()
    return t    