from supply_assistant import app, config
from supply_assistant import notification_bot

if __name__ == '__main__':
    notification_bot.run()
    app.run(debug=False, port=config["SITE"]["port"])
