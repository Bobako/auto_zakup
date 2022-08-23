# supply_assistant

Сайт, предназначенный для помощи в создании и отправки заказов поставщикам ресторана.
Юз-кейс (в общем и целом): менеджер создает заказ (или изменяет предыдущий), где перечисляет все необходимые
товары. Администратор получает уведомления и подтверждает заказ. Бот отправляет в телеграм чат с поставщиком всю
необходимую информацию о заказе.

Вокруг этого ключевого функционала созданы более мелкие функции, подробнее в тз.

[ТЗ на проект](task.md)

Проект написан давно и не соответствует тому уровню качества кода, которого я стараюсь держаться на данный момент, о
нынешней ситуации лучше дадут понять более новые репозитории,
например [github.com/Bobako/sms_handler](https://github.com/Bobako/sms_handler).
В ближайшее время я скорее всего проведу рефакторинг проекта, чтобы он соответствовал приемлемому уровню.

Инструменты, использованные в проекте:

- Python (Flask, SQLAlchemy, TelegramBotAPI, а также менее значимые библиотеки)
- HTML, CSS, JS (JQuery)

Потрогать демку проекта можно [тут](http://bobako.site/supply_assistant/). Вход по ключу 0000.
В демонстрационной версии БД заполнена случайными данными, бот доступен
по [ссылке](http://t.me/supply_assistant_demo_bot). Демка развернута на Ubuntu 20.04 средствами NGINX, Gunicorn,
Supervisord.