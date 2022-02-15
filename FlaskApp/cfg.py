prod = True

BOT_TOKEN = "2104797267:AAFp-FX16r1-nogBbN26Zztk9mGGOGLUoP4"

DEFAULT_ORDER_FORMAT = """Добрый день<br>
<br>
Заказ #{{order.id}} для {{order.facility.name}} ({{order.facility.address}})<br>
<br>
{%for product in order.products %}{% if product.amount %}{%if vendor.id == product.vendor_id%}
{{product.product.name}}: {{product.amount}} {{product.unit.designation}} {% if not product.official %}(не официально){% endif %}<br>
{%endif%}{%endif%}{%endfor%}
<br>
Спасибо"""


if prod:
    DB_STRING = "sqlite:////var/www/FlaskApp/database.db"
    UPLOAD = "/var/www/FlaskApp/upload"
    FORMAT_PATH = "/var/www/FlaskApp/FlaskApp/templates/formatted_order.html"
    LOGS_PATH = "/var/www/FlaskApp/access_log.txt"
else:
    DB_STRING = "sqlite:///database.db"
    UPLOAD = "upload"
    FORMAT_PATH = "FlaskApp/templates/formatted_order.html"
    LOGS_PATH = "access_log.txt"
