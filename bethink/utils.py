import telebot
import socket


def tg_send(tg_message, chat_id):
    if socket.gethostname()=='DESKTOP-VRFTRN7':
        from telebot import apihelper
        apihelper.proxy = {'https': 'socks5://127.0.0.1:1080'}

    bot_token = '755252536:AAEWGnVSWq7RH_Z3Lpbn10k5Qwhhb3lopPA'

    tb = telebot.TeleBot(bot_token)

    tb.send_message(chat_id, tg_message)
