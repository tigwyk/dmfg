from celery import Celery
from .models import Trade
from .database import db

def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

def process_open_trades(trade=None):
    if trade.order_type == 'B':
        compatibles = Trade.query.filter_by(order_type='S')
    elif trade.order_type == 'S':
        compatibles = Trade.query.filter_by(order_type='B')
    else compatibles = Trade.query.all()
    immediates = compatibles.query.filter_by(price=trade.price)
    if immediates:
        if trade.order_type == 'S':
            seller = trade.user
            buyer = immediates.query.all.first().user
            buy_qty = immediates.query.all.first().quantity
            buy_price = immediates.query.all.first().price
            sell_qty = trade.quantity
            new_quantity = sell_qty - buy_qty
            total_price = buy_price * buy_qty
            buyer.money = buyer.money - total_price
            trade.user.money = trade.user.money + total_price
            trade.quantity = new_quantity
            
            
    