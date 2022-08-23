from supply_assistant import app, config
from supply_assistant import bot

if __name__ == '__main__':
    bot.run()
    app.run(debug=False, port=config["SITE"]["port"])
