from FlaskApp import app as application

if __name__ == '__main__':
    application.secret_key = b'lol'
    application.run(debug=True)
