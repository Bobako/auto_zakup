from FlaskApp import app as application
from FlaskApp import bot

if __name__ == '__main__':
    application.secret_key = b'lol'
    bot.run()
    application.run(debug=True)
