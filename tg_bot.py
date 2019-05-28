import os
import re
import socket
from dateutil import parser
from dateutil.utils import default_tzinfo
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "siteengine.settings")
import django
import telebot
from datetime import datetime, timedelta
import pytz     # $ pip install pytz
django.setup()
# your imports, e.g. Django models
from bethink.models.card import Card
from django.contrib.auth.models import User
from django.utils.timezone import localtime

t = Card.objects.all()

bot_token = ''

if socket.gethostname() == 'DESKTOP-VRFTRN7':
    from telebot import apihelper
    apihelper.proxy = {'https': 'socks5://127.0.0.1:1080'}
    bot_token = ''


tb = telebot.TeleBot(bot_token)


@tb.message_handler(commands=['start', 'help'])
def send_welcome(message):

    # message.chat.id
    usr = User.objects.filter(profile__tg_id=message.chat.id)
    if usr:
        tb.reply_to(message, "Привет, {0} ".format(usr[0].first_name))
    else:
        tb.reply_to(message, "Привет! ✌️Нужно немного настроек.\n"
                             "Если еще не зарегистрированы - зарегистрируйтесь на bethink.servapp.ru \n"
                             "Затем укажите в профиле ID чата: {0}".format(message.chat.id))

@tb.message_handler(func=lambda m: True)
def handle_text(message):
    text = message.text.lower()
    hours = []
    minutes = []
    what = []

    when = re.findall(r'(?<=через).*$', text) # Если указан промежуток
    if when:
        if re.findall(r'час', when[0]):
            minutes = re.findall(r'(?<=часа)(.*)(?=минут)', when[0])
            hours = re.findall(r'.+?(?=час)', when[0])
        else:
            minutes = re.findall(r'.+?(?=минут)', when[0])

        if len(hours) > 0:
            hours = int(hours[0])
        else:
            hours = 0

        if len(minutes) > 0:
            minutes = int(minutes[0])
        else:
            minutes = 0

        what = re.findall(r'.+?(?=через)', text)

    in_time = re.findall(r'в([^в]+)$', text)  # Если указано точное время
    if in_time:
        from dateutil.tz import gettz
        tzinfos = {"CST": gettz("UTC")}
        dt = parser.parse(in_time[0] + ' CST', tzinfos=tzinfos)
        what = re.findall(r'((?s)((^.*)в))(.*$)', text)
        if what:
            what = what[0][2]


    t=1
    #notification_dt = datetime.now(pytz.utc) + timedelta(minutes=minutes+hours*60)
    #local_dt = localtime(notification_dt)



tb.polling()

