from threading import Thread
import sys
from telebot import TeleBot

sys.path.append("./cfg.py")
sys.path.append("./db_handler.py")

from cfg import *
from db_handler import Noti

bot = TeleBot(BOT_TOKEN)


class Bot:
    def __init__(self, session):
        self.session = session

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
            return str(type(e)) + " " + str(e.args)
        else:
            return True
