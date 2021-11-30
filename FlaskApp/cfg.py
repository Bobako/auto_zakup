BOT_TOKEN = "2104797267:AAFp-FX16r1-nogBbN26Zztk9mGGOGLUoP4"

DB_STRING = "sqlite:///FlaskApp/database.db"

DEFAULT_ORDER_FORMAT = """Добрый день<br>
<br>
Заказ #{{order.id}} для {{order.facility.name}} ({{order.facility.address}})<br>
<br>
{%for product in order.products %}{% if product.amount %}{%if vendor in product.product.vendors%}
{{product.product.name}}: {{product.amount}} {{product.product.unit.designation}}<br>
{%endif%}{%endif%}{%endfor%}
<br>
Спасибо"""
