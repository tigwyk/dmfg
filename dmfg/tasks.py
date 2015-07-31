# -*- coding: utf-8 -*-
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
    immediates = Trade.query.filter_by(order_type=('S' if trade.order_type=='B' else 'B'),price=trade.price,item=trade.item).all()
    the_rest = Trade.query.filter_by(order_type=('S' if trade.order_type=='B' else 'B'),item=trade.item).all()
    the_rest =  [x for x in the_rest if x not in immediates]
    if immediates:
        if trade.order_type == 'S':
            for immediate_trade in immediates:
                seller = trade.user
                buyer = immediate_trade.user
                buy_qty = immediate_trade.quantity
                buy_price = immediate_trade.price
                sell_qty = trade.quantity
                new_quantity = sell_qty - buy_qty
                if new_quantity < 0:
                    break
                total_price = buy_price * buy_qty
                if not buyer.withdraw_funds(total_price):
                    break
                seller.deposit_funds(total_price)
                trade.quantity = new_quantity
                buyer.add_item(trade.item.id, buy_qty)
                seller.remove_item(trade.item.id, buy_qty)
                db.session.delete(immediate_trade)
                if trade.quantity == 0:
                    db.session.delete(trade)
        elif trade.order_type == 'B':
            for immediate_trade in immediates:
                buyer = trade.user
                seller = immediate_trade.user
                sell_qty = immediate_trade.quantity
                buy_price = trade.price
                buy_qty = trade.quantity    
                new_quantity = sell_qty - buy_qty
                if new_quantity < 0:
                    break
                total_price = buy_price * buy_qty
                if not buyer.withdraw_funds(total_price):
                    break
                seller.deposit_funds(total_price)
                immediate_trade.quantity = new_quantity
                buyer.add_item(trade.item.id, buy_qty)
                seller.remove_item(trade.item.id, buy_qty)
                db.session.delete(trade)
                if immediate_trade.quantity == 0:
                    db.session.delete(immediate_trade)            
        else:
            pass        
        db.session.commit()
    elif the_rest:
        if trade.order_type == 'S':
            for immediate_trade in the_rest:
                seller = trade.user
                buyer = immediate_trade.user
                buy_qty = immediate_trade.quantity
                buy_price = immediate_trade.price
                sell_price = trade.price
                sell_qty = trade.quantity
                new_quantity = sell_qty - buy_qty
                if new_quantity < 0:
                    break
                total_price = buy_price * buy_qty
                if sell_price < buy_price:
                    break
                if not buyer.withdraw_funds(total_price):
                    break
                seller.deposit_funds(total_price)
                trade.quantity = new_quantity
                buyer.add_item(trade.item.id, buy_qty)
                seller.remove_item(trade.item.id, buy_qty)
                db.session.delete(immediate_trade)
                if trade.quantity == 0:
                    db.session.delete(trade)
            elif trade.order_type == 'B':
                for immediate_trade in the_rest:
                    buyer = trade.user
                    seller = immediate_trade.user
                    sell_qty = immediate_trade.quantity
                    buy_price = trade.price
                    sell_price = immediate_trade.price
                    buy_qty = trade.quantity    
                    new_quantity = sell_qty - buy_qty
                    if new_quantity < 0:
                        break
                    total_price = buy_price * buy_qty
                    if buy_price < sell_price:
                        break
                    if not buyer.withdraw_funds(total_price):
                        break
                    seller.deposit_funds(total_price)
                    immediate_trade.quantity = new_quantity
                    buyer.add_item(trade.item.id, buy_qty)
                    seller.remove_item(trade.item.id, buy_qty)
                    db.session.delete(trade)
                    if immediate_trade.quantity == 0:
                        db.session.delete(immediate_trade)            
    db.session.commit()        
            
            
    