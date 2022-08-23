import datetime

from supply_assistant import db, login_manager


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    position = db.Column(db.String)
    facility_id = db.Column(db.Integer)
    code = db.Column(db.String)
    is_admin = db.Column(db.Boolean)

    is_authenticated = db.Column(db.Boolean)
    is_active = True
    is_anonymous = False

    def __init__(self, name, surname, position, facilities, code, is_admin):
        self.name = name
        self.surname = surname
        self.position = position
        self.facilities = facilities
        self.code = code
        self.is_authenticated = False
        self.is_admin = is_admin

    def get_id(self):
        return self.id


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Facility(db.Model):
    __tablename__ = "facility"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)
    tg_id = db.Column(db.Integer)
    users = db.relationship('User', secondary='user_facilities_association', lazy='dynamic', backref='facilities')

    def __init__(self, name, address, tg_id):
        self.name = name
        self.address = address
        self.tg_id = tg_id


class Vendor(db.Model):
    __tablename__ = "vendor"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer)
    tg_id = db.Column(db.Integer)
    schedule = db.Column(db.Integer)
    products = db.relationship('Product', secondary='products_association', lazy='dynamic', backref='vendors')
    facilities = db.relationship('Facility', secondary='facilities_association', lazy='dynamic', backref='vendors')

    def get_sch(self):
        if self.schedule:
            if "День" not in str(self.schedule):
                return list(map(int, list(str(self.schedule))))
        return [8]

    def __init__(self, name, tg_id, schedule, products=None, facilities=None):
        self.name = name
        self.tg_id = tg_id
        self.schedule = schedule
        self.products = products
        self.facilities = facilities


user_facilities_association = db.Table(
    'user_facilities_association', db.metadata,
    db.Column('facility_id', db.Integer(), db.ForeignKey('facility.id'), primary_key=True),
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id'), primary_key=True),
)

facilities_association = db.Table(
    'facilities_association', db.metadata,
    db.Column('facility_id', db.Integer(), db.ForeignKey('facility.id'), primary_key=True),
    db.Column('vendor_id', db.Integer(), db.ForeignKey('vendor.id'), primary_key=True),
)

products_association = db.Table(
    'products_association', db.metadata,
    db.Column('product_id', db.Integer(), db.ForeignKey('product.id'), primary_key=True),
    db.Column('vendor_id', db.Integer(), db.ForeignKey('vendor.id'), primary_key=True),
)


class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    unit_id = db.Column(db.Integer, db.ForeignKey("unit.id"))
    unit = db.relationship("Unit", backref="products")
    orders_count = db.Column(db.Integer)
    orders_amount = db.Column(db.Float)
    alco = db.Column(db.Boolean)

    def __init__(self, name, unit_id, alco):
        self.name = name
        self.unit_id = unit_id
        self.orders_count = 0
        self.orders_amount = 0
        self.alco = alco


class Unit(db.Model):
    __tablename__ = "unit"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    designation = db.Column(db.String)

    def __init__(self, name, designation):
        self.name = name
        self.designation = designation


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    create_date = db.Column(db.DateTime)
    sent_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref="orders")
    facility_id = db.Column(db.Integer, db.ForeignKey("facility.id"))
    facility = db.relationship("Facility", backref="orders")
    status = db.Column(db.String)  # NEW or ADDITIONAL or ORDERED
    msg_id = db.Column(db.Integer)
    updated = db.Column(db.Boolean)
    msg = db.Column(db.String)
    display = db.Column(db.Boolean)
    copy_id = db.Column(db.Integer)
    deleted = db.Column(db.Boolean)
    delete_date = db.Column(db.DateTime)

    def __init__(self, user_id, facility_id, date=None, status="NEW", display=True):
        self.create_date = datetime.datetime.now()
        self.date = self.create_date + datetime.timedelta(days=1)  # supply date, wasn't used
        self.user_id = user_id
        self.facility_id = facility_id
        self.status = status
        self.msg_id = None
        self.updated = False
        self.msg = None
        self.display = display
        self.deleted = False
        self.delete_date = None
        self.sent_date = None


class OrderedProduct(db.Model):
    __tablename__ = "ordered_product"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    order = db.relationship("Order", backref="products")
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    product = db.relationship("Product", backref="ordered")
    vendor_id = db.Column(db.Integer, db.ForeignKey("vendor.id"))
    vendor = db.relationship("Vendor", backref="ordered")
    amount = db.Column(db.Float, nullable=True)
    unit_id = db.Column(db.Integer, db.ForeignKey("unit.id"))
    unit = db.relationship("Unit", backref="ordered")
    official = db.Column(db.Boolean)

    def __init__(self, product_id, amount, vendor_id, order_id, unit_id, official):
        self.product_id = product_id
        self.amount = amount
        self.vendor_id = vendor_id
        self.order_id = order_id
        self.unit_id = unit_id
        self.official = official

    def __repr__(self):
        return f"{self.product.name} {self.amount}"


class MSGFormat(db.Model):  # jinja2 template of message to supplyer
    __tablename__ = "msg"
    msg = db.Column(db.String, primary_key=True)

    def __init__(self, msg):
        self.msg = msg


class Noti(db.Model):  # Notifications settings
    __tablename__ = "noti"
    id = db.Column(db.Integer, primary_key=True)
    tg_id = db.Column(db.Integer)
    send = db.Column(db.Boolean)

    def __init__(self):
        self.tg_id = 0
        self.send = False
