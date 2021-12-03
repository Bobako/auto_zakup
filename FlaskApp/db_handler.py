import datetime
import sys

import sqlalchemy
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from FlaskApp.cfg import *

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    position = Column(String)
    facility_id = Column(Integer, ForeignKey("facility.id"))
    facility = relationship("Facility", backref="users")
    code = Column(String)
    is_admin = Column(Boolean)

    is_authenticated = Column(Boolean)
    is_active = True
    is_anonymous = False

    def __repr__(self):
        return f"#{self.id} {self.name} {self.surname} - {self.position}; {self.is_authenticated}"

    def __init__(self, name, surname, position, facility_id, code, is_admin):
        self.name = name
        self.surname = surname
        self.position = position
        self.facility_id = facility_id
        self.code = code
        self.is_authenticated = False
        self.is_admin = is_admin

    def get_id(self):
        return self.id


class Facility(Base):
    __tablename__ = "facility"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)

    def __init__(self, name, address):
        self.name = name
        self.address = address


class Vendor(Base):
    __tablename__ = "vendor"
    id = Column(Integer, primary_key=True)
    name = Column(Integer)
    tg_id = Column(Integer)
    schedule = Column(Integer)
    products = relationship('Product', secondary='products_association', lazy='dynamic', backref='vendors')
    facilities = relationship('Facility', secondary='facilities_association', lazy='dynamic', backref='vendors')

    def get_sch(self):
        if self.schedule:
            if "День" not in str(self.schedule):
                return list(map(int, list(str(self.schedule))))
        return [8]

    def __init__(self, name, tg_id, schedule, products=None, facilities=None):
        self.name = name
        self.tg_id = tg_id
        self.schedule = schedule
        if products:
            self.products = products
        if facilities:
            self.facilities = facilities


facilities_association = Table(
    'facilities_association', Base.metadata,
    Column('facility_id', Integer(), ForeignKey('facility.id'), primary_key=True),
    Column('vendor_id', Integer(), ForeignKey('vendor.id'), primary_key=True),
)

products_association = Table(
    'products_association', Base.metadata,
    Column('product_id', Integer(), ForeignKey('product.id'), primary_key=True),
    Column('vendor_id', Integer(), ForeignKey('vendor.id'), primary_key=True),
)


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    unit_id = Column(Integer, ForeignKey("unit.id"))
    unit = relationship("Unit", backref="products")
    orders_count = Column(Integer)
    orders_amount = Column(Integer)

    def __init__(self, name, unit_id):
        self.name = name
        self.unit_id = unit_id
        self.orders_count = 0
        self.orders_amount = 0


class Unit(Base):
    __tablename__ = "unit"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    designation = Column(String)

    def __init__(self, name, designation):
        self.name = name
        self.designation = designation


class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    create_date = Column(DateTime)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", backref="orders")
    facility_id = Column(Integer, ForeignKey("facility.id"))
    facility = relationship("Facility", backref="orders")
    status = Column(String)  # NEW or ADDITIONAL or ORDERED
    msg_id = Column(Integer)
    updated = Column(Boolean)
    msg = Column(String)

    def __init__(self, user_id, facility_id, date=None, status="NEW"):
        self.create_date = datetime.datetime.now()
        self.date = self.create_date + datetime.timedelta(days=1)
        self.user_id = user_id
        self.facility_id = facility_id
        self.status = status
        self.msg_id = None
        self.updated = False
        self.msg = None


class OrderedProduct(Base):
    __tablename__ = "ordered_product"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("order.id"))
    order = relationship("Order", backref="products")
    product_id = Column(Integer, ForeignKey("product.id"))
    product = relationship("Product", backref="ordered")
    vendor_id = Column(Integer, ForeignKey("vendor.id"))
    vendor = relationship("Vendor", backref="ordered")
    amount = Column(Integer)

    def __init__(self, product_id, amount, vendor_id, order_id):
        self.product_id = product_id
        self.amount = amount
        self.vendor_id = vendor_id
        self.order_id = order_id

    def __repr__(self):
        return f"{self.product.name} {self.amount}"


class MSGFormat(Base):
    __tablename__ = "msg"
    msg = Column(String, primary_key=True)

    def __init__(self, msg):
        self.msg = msg


class Noti(Base):
    __tablename__ = "noti"
    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer)
    send = Column(Boolean)

    def __init__(self):
        self.tg_id = 0
        self.send = False


class Handler:
    session: sqlalchemy.orm.session.Session
    exist: bool

    def __init__(self, base=Base):
        self.db_exist()
        engine = sqlalchemy.create_engine(DB_STRING + '?check_same_thread=False')
        base.metadata.create_all(engine)
        self.session = sessionmaker(bind=engine, expire_on_commit=False)()
        if not self.exist:
            self.create_admin()
        print("База данных подключена.")

    def db_exist(self):
        db_path = DB_STRING.split("///")[-1]
        try:
            with open(db_path, "r"):
                pass
        except FileNotFoundError:
            self.exist = False
        else:
            self.exist = True

    def create_admin(self):
        self.session.add(User("Админ", "", "", None, "0000", True))
        self.session.add(MSGFormat(DEFAULT_ORDER_FORMAT))
        self.session.add(Noti())
        self.session.commit()


def delete_products(base=Base):
    engine = sqlalchemy.create_engine('sqlite:///FlaskApp/database.db')
    base.metadata.create_all(engine)
    session = sessionmaker(bind=engine, expire_on_commit=False)()
    for product in session.query(Product).all():
        session.delete(product)
    session.commit()


if __name__ == '__main__':
    pass
