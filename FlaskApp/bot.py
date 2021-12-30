from threading import Thread
import sys
from telebot import TeleBot

from FlaskApp.cfg import *
from FlaskApp.db_handler import Noti

bot = TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["id"])
def id_(message):
    bot.send_message(message.chat.id, str(message.chat.id))


class Bot:
    def __init__(self, session):
        self.session = session

    def run(self):
        print("bot is running")
        t = Thread(target=self.loop)
        t.start()

    def loop(self):
        while True:
            try:
                bot.polling(none_stop=True, interval=0)
            except Exception:
                pass

    def noti_admin(self, msg):
        noti = self.session.query(Noti).one()
        if noti.send:
            try:
                bot.send_message(noti.tg_id, msg)
            except Exception as e:
                print(type(e), e.args, "при отправке админу")
                return str(type(e)) + " " + str(e.args)
            else:
                return True

    def noti_vendor(self, id_, msg):
        try:
            bot.send_message(id_, msg)
        except Exception as e:
            print(type(e), e.args, "при отправке поставщику")
            return str(type(e)) + " " + str(e.args) + " " + str(e)
        else:
            return str(True)
