import os

from flask import Flask, render_template, request, flash, redirect, url_for
from sqlalchemy import exc, desc, asc
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
import openpyxl

from FlaskApp.db_handler import *
from FlaskApp.bot import Bot

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD
db = Handler()
login_manager = LoginManager()
login_manager.init_app(app)
bot = Bot(db.session)

DAYS = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("login") + f"?next={request.url}")


@login_manager.user_loader
def load_user(user_id):
    try:
        user = db.session.query(User).filter(User.id == user_id).one()
        return user
    except exc.NoResultFound:
        return None


@app.route("/login", methods=['post', 'get'])
def login():
    if current_user:
        db_logout(current_user)
    if request.method == "POST":
        code = request.form.get("code")
        try:
            user = db.session.query(User).filter(User.code == code).one()
        except exc.NoResultFound:
            flash("Некорректный код")
        else:
            db_login(user)
            next_page = request.args.get('next')
            if not next_page:
                next_page = url_for('index')
            return redirect(next_page)

    return render_template("login.html")


@app.route("/users", methods=['post', 'get'])
@login_required
def users_page():
    user = current_user
    if not user.is_admin:
        return redirect(url_for("index"))
    if request.method == 'POST':
        users = parse_forms(request.form, ["is_admin"])
        for user in users.values():
            if user["facility_name"] == "Заведение":
                user["facility_id"] = None
            else:
                user["facility_id"] = db.session.query(Facility).filter(Facility.name == user["facility_name"]).one().id
            user.pop("facility_name")
        users[str(current_user.id)]["is_admin"] = True
        try:
            users[str(current_user.id)].pop("delete")
        except KeyError:
            pass
        pins = []
        correct = True
        for user in users.values():
            if user["code"] in pins:
                flash("Пин коды должны быть уникальны")
                correct = False
                break
            else:
                pins.append(user["code"])
        if correct:
            update_objs(users, User)
    return render_template("users.html", users=db.session.query(User).all(),
                           facilities=db.session.query(Facility).all())


@app.route("/facilities", methods=['post', 'get'])
@login_required
def facilities_page():
    user = current_user
    if not user.is_admin:
        return redirect(url_for("index"))
    if request.method == 'POST':
        facilities = parse_forms(request.form)
        names = []
        correct = True
        for facility in facilities.values():
            if facility["name"] in names:
                flash("Названия должны быть уникальны")
                correct = False
                break
            else:
                names.append(facility["name"])
        if correct:
            update_objs(facilities, Facility)
    return render_template("facilities.html", facilities=db.session.query(Facility).all())


@app.route("/units", methods=['post', 'get'])
@login_required
def units_page():
    user = current_user
    if not user.is_admin:
        return redirect(url_for("index"))
    if request.method == "POST":
        units = parse_forms(request.form)

        deses = []
        correct = True
        for unit in units.values():
            if unit["designation"] in deses:
                flash("Обозначения должны быть уникальны")
                correct = False
                break
            else:
                deses.append(unit["designation"])
        if correct:
            update_objs(units, Unit)
    return render_template("units.html", units=db.session.query(Unit).all())


@app.route("/products", methods=['post', 'get'])
@login_required
def products_page():
    user = current_user
    if not user.is_admin:
        return redirect(url_for("index"))
    if request.method == "POST":
        products = parse_forms(request.form)
        if "products" in products:
            products.pop("products")
        for product in products.values():
            if product["unit_designation"] == "Единицы измерения":
                product["unit_id"] = None
            else:
                product["unit_id"] = db.session.query(Unit).filter(
                    Unit.designation == product["unit_designation"]).one().id
            product.pop("unit_designation")

        update_objs(products, Product)
        file = request.files["products:file"]
        if file:
            filename = "file.xlsx"
            try:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                parse_file(UPLOAD+"/"+filename)
            except Exception as ex:
                return ex
            finally:
                os.remove(UPLOAD+"/"+filename)

    return render_template("products.html", products=db.session.query(Product).all(),
                           units=db.session.query(Unit).all())


def parse_file(filename):
    wb = openpyxl.load_workbook(filename)
    sheet = wb["Постачальники"]
    row = 2
    while sheet.cell(row=row, column=1).value:
        product_name = sheet.cell(row=row, column=1).value
        vendor_name = sheet.cell(row=row, column=6).value
        if not db.session.query(Product).filter(Product.name == product_name).first():
            product = Product(product_name, None)
            db.session.add(product)
            if vendor := db.session.query(Vendor).filter(Vendor.name == vendor_name).first():
                vendor.products.append(product)

        row += 1
    wb.close()
    db.session.commit()




@app.route("/vendors", methods=['post', 'get'])
@login_required
def vendors_page():
    user = current_user
    if not user.is_admin:
        return redirect(url_for("index"))

    if request.method == "POST":
        vendors = parse_forms(request.form)

        for vendor in vendors.values():
            vendor["products"] = []
            for product_id in vendor['products_ids'].split(":"):
                if product_id:
                    if (product := db.session.query(Product).filter(
                            Product.id == product_id).one()) not in vendor["products"]:
                        vendor["products"].append(product)
            schedule = ''
            for key in vendor:
                if "schedule" in key:
                    schedule += key[-1]
            if schedule != '':
                vendor["schedule"] = int(schedule)
            else:
                vendor["schedule"] = None
            vendor["facilities"] = []
            for facility_id in vendor['facilities_ids'].split(":"):
                if facility_id:
                    if (facility := db.session.query(Facility).filter(
                            Facility.id == facility_id).one()) not in vendor["facilities"]:
                        vendor["facilities"].append(facility)
            vendor.pop('products_ids')
            vendor.pop('facilities_ids')
            for i in range(7):
                if "schedule" + str(i) in vendor:
                    vendor.pop("schedule" + str(i))
        update_objs(vendors, Vendor)

    return render_template("vendors.html", vendors=db.session.query(Vendor).all(),
                           facilities=db.session.query(Facility).all(),
                           products=db.session.query(Product).all(), days=DAYS)


@app.route("/preview", methods=['post', 'get'])
@login_required
def preview():
    user = current_user
    if not user.is_admin:
        return redirect(url_for("index"))
    order_id = request.args.get('id')
    order = db.session.query(Order).filter(Order.id == order_id).one()
    if request.method == "POST":
        if not request.form.get("order:confirm"):
            return redirect(url_for("index"))

        msgs = parse_forms(request.form)
        msgs.pop("order")
        order.status = "ORDERED"
        send_order(order, msgs)
        db.session.commit()
        return redirect(url_for("index"))

    msg = db.session.query(MSGFormat).one().msg
    vendors = []
    for product in order.products:
        if product.amount:
            vendors.append(product.vendor)

    return render_template("preview.html", order=order, vendors=vendors)


def send_order(order, msgs):  # msgs - {vendor.id:msg}
    for product in order.products:
        if product.amount:
            product.product.orders_count += 1
            product.product.orders_amount += product.amount
    db.session.commit()
    for vendor_id, msg in msgs.items():
        id_ = db.session.query(Vendor).filter(Vendor.id == vendor_id).one().tg_id
        bot.noti_vendor(int(id_), msg['msg'])


@app.route("/order_format", methods=['post', 'get'])
@login_required
def order_format():
    user = current_user
    if not user.is_admin:
        return redirect(url_for("index"))
    if request.method == "POST":
        if request.form.get("default"):
            msg = DEFAULT_ORDER_FORMAT
        elif request.form.get("confirm"):
            msg = request.form.get("msg")
        msg = msg.replace("}\n", "}")
        db.session.query(MSGFormat).one().msg = msg
        db.session.commit()
        with open("/var/www/FlaskApp/FlaskApp/templates/formatted_order.html", "w", encoding='utf-8') as file:
            file.write(msg)
    msg = db.session.query(MSGFormat).one().msg
    return render_template("order_format.html", msg=msg)


@app.route("/", methods=['post', 'get'])
@login_required
def index():
    user = current_user
    if request.method == 'POST':
        order = parse_forms(request.form)
        order_id = list(order["order"].keys())[1]
        if order_id == "new":
            order_id = create_order(order, user)
        else:
            order_id = update_order(order, order_id)

        if user.is_admin and order_id:
            return redirect(url_for("preview") + f"?id={order_id}")

    orders = get_orders(user)
    old_orders = get_old_orders(user)

    return render_template("orders.html", user=user, orders=orders, old_orders=old_orders,
                           products=db.session.query(Product).all(), days=DAYS,
                           vendors=db.session.query(Vendor).all(), facilities=db.session.query(Facility).all())


def get_orders(user):
    if user.is_admin:
        orders = db.session.query(Order).order_by(desc(Order.create_date)).filter(Order.status == "NEW").filter(
            Order.date > datetime.datetime.now()).all()
        orders += db.session.query(Order).order_by(desc(Order.create_date)).filter(Order.status == "ADDITIONAL").filter(
            Order.date > datetime.datetime.now()).all()
        orders += db.session.query(Order).order_by(desc(Order.create_date)).filter(Order.status == "ORDERED").filter(
            Order.date > datetime.datetime.now()).all()
    else:
        orders = db.session.query(Order).filter(Order.facility_id == user.facility_id).order_by(
            desc(Order.create_date)).filter(Order.date > datetime.datetime.now()).all()
    return orders


def get_old_orders(user):
    if user.is_admin:
        orders = db.session.query(Order).order_by(desc(Order.create_date)).filter(
            Order.date < datetime.datetime.now()).all()


def create_order(order, user):
    facility_id = order["order"]["facility_id"]
    order.pop("order")
    db.session.add(Order(user.id, facility_id))
    db.session.commit()
    order_id = db.session.query(Order).order_by(desc(Order.id)).first().id
    parse_order_products(order, order_id)
    bot.noti_admin(f"Создан заказ {order_id}")
    return order_id


def parse_order_products(order, order_id):
    for product_id, product_dict in order.items():
        if "NEW" in product_id:
            db.session.add(OrderedProduct(product_dict["product_id"], product_dict["amount"], product_dict["vendor_id"],
                                          order_id))
        else:
            product = db.session.query(OrderedProduct).filter(OrderedProduct.id == product_id).one()
            product.amount = product_dict["amount"]
    db.session.commit()


def update_order(order, order_id):
    if "Удалить" in order["order"].values():
        order_obj = db.session.query(Order).filter(Order.id == order_id).one()
        for product in order_obj.products:
            db.session.delete(product)
        db.session.delete(order_obj)
        db.session.commit()
        return None
    order.pop("order")
    parse_order_products(order, order_id)
    order_obj = db.session.query(Order).filter(Order.id == order_id).one()
    order_obj.status = "ADDITIONAL"
    db.session.commit()
    bot.noti_admin(f"Изменен заказ {order_id}")
    return order_id


@app.route("/api/available_products", methods=['get'])
def get_available_products():
    facility_id = request.args.get('id')
    return render_template('order_form.html',
                           vendors=db.session.query(Facility).filter(Facility.id == facility_id).one().vendors)


@app.route("/api/formatted_order", methods=['get'])
def formatted_order():
    order_id = request.args.get('oid')
    order = db.session.query(Order).filter(Order.id == order_id).one()
    vendor = db.session.query(Vendor).filter(Vendor.id == request.args.get('vid')).one()
    return render_template('formatted_order.html',
                           order=order, vendor=vendor).replace("\n", "").replace("<br>", "\n")


@app.route("/orders_admin", methods=['post', 'get'])
@login_required
def orders_admin_page():
    return


def merge_sort(stats: list, func):
    l = len(stats)
    if l < 2:
        return stats
    stats1 = merge_sort(stats[:int(l / 2)], func)
    stats2 = merge_sort(stats[int(l / 2):], func)

    i1 = 0
    i2 = 0
    stats = []
    while i1 < len(stats1) or i2 < len(stats2):
        if i1 == len(stats1):
            stats.append(stats2[i2])
            i2 += 1
        elif i2 == len(stats2):
            stats.append(stats1[i1])
            i1 += 1
        else:
            if func(stats1[i1], stats2[i2]) < 0:
                stats.append(stats1[i1])
                i1 += 1
            else:
                stats.append(stats2[i2])
                i2 += 1
    return stats


def less(stats1, stats2):
    return stats1[2] - stats2[2]


def more(stats1, stats2):
    return stats2[2] - stats1[2]


sf = less


@app.route("/stats", methods=['post', 'get'])
@login_required
def stats_page():
    global sf
    if request.method == "POST":
        if sf == less:
            sf = more
        else:
            sf = less
    stats = []
    for vendor in db.session.query(Vendor).all():
        for product in vendor.products:
            if orders := db.session.query(OrderedProduct).filter(OrderedProduct.product_id == product.id).all():
                stats.append(
                    [f"{product.name} ({vendor.name})", sum([bool(order.amount) for order in orders]),
                     sum([order.amount for order in orders]),
                     product.unit.designation])
            else:
                stats.append([f"{product.name} ({vendor.name})", 0, 0, product.unit.designation])
    print(stats)
    return render_template("stats.html",
                           products=merge_sort(stats, sf))


@app.route("/logs", methods=['post', 'get'])
@login_required
def logs_page():
    return


@app.route("/notifications", methods=['post', 'get'])
@login_required
def noti_page():
    if request.method == "POST":
        noti = db.session.query(Noti).one()
        noti.tg_id = request.form.get("tg_id")
        noti.send = bool(request.form.get("send"))
        db.session.commit()
    return render_template("noti.html", noti=db.session.query(Noti).one())


def db_login(user):
    login_user(user)
    user.is_authenticated = True
    db.session.commit()


def db_logout(user):
    logout_user()
    db.session.commit()


def parse_forms(form, checkboxes=()):
    result = {}

    for key, val in form.lists():
        id_, arg = key.split(":")
        if id_ == "NEW":
            for i, value in enumerate(val):
                id_ = "NEW" + str(i)
                if id_ not in result:
                    result[id_] = dict()
                result[id_][arg] = value
        else:
            val = val[0]
            if id_ not in result:
                result[id_] = dict()

            if val == "on":
                val = True
            result[id_][arg] = val

    for res_dict in result.values():
        for checkbox in checkboxes:
            if checkbox not in res_dict:
                res_dict[checkbox] = False

    return result


def update_objs(dicts, class_, not_nullable="name"):
    for id_, dict_ in dicts.items():
        if "NEW" not in id_:
            obj = db.session.query(class_).filter(class_.id == id_).one()
            if "delete" in dict_:
                db.session.delete(obj)
                continue
            for arg_name, value in dict_.items():
                setattr(obj, arg_name, value)
        else:
            if not dict_[not_nullable]:
                continue

            obj = class_(**dict_)
            db.session.add(obj)
    db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)
