import datetime

from supply_assistant.models import User, MSGFormat, Noti, Order, Product
from supply_assistant.cfg import config


def initialize(session):
    """Create default rows in db, if it was created just now"""
    if not session.query(User).first():
        session.add(User("Админ", "", "", [], "0000", True))
        session.add(MSGFormat(config["DEFAULT"]["message_format"]))
        session.add(Noti())
        session.commit()


def drop_orders(session):
    """Drop orders, which have been marked as deleted for long time(specified in config.ini)"""
    orders = session.query(Order).filter(
        Order.deleted == True).filter(
        Order.delete_date < datetime.datetime.now() - datetime.timedelta(
            days=config["DATABASE"]["marked_orders_deletion_period_days"])).all()
    for order in orders:
        session.delete(order)
    session.commit()


def drop_duplicates(session):
    products = session.query(Product).all()
    unique = {}  # name: product
    for product in products:
        if product.name in unique:
            # for vendor in product.vendors: # TODO chego blyat
            #    unique[product.name].vendors.append(vendor)
            session.delete(product)
        else:
            unique[product.name] = product
    session.commit()
