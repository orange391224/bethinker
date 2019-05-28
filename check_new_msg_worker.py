import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "siteengine.settings")
import django
django.setup()
from bethink.models.tgmessage import TgMessage
from bethink.utils import tg_send
from datetime import datetime
from time import sleep
import pytz



def check_new_message_task():
    for message in TgMessage.objects.filter(sent_date__isnull=True):
        """
        card = Card.objects.filter(pk=message.card_id)[0]
        if not card:  # Если карту удалили, значит сообщение по ней нужно так же удалить
            message.delete()
            continue
        print('Отправка: {0} \n {1}'.format(card[0].title, card[0].body))
        tg_send('{0} \n {1}'.format(card[0].title, card[0].body), card[0].user.profile.tg_id)
        """
        # current_datetime = datetime.now(tz=pytz.timezone('Asia/Krasnoyarsk'))
        # tz=message.notification_date.tzinfo
        current_datetime = datetime.now(tz=pytz.timezone('UTC'))

        if current_datetime < message.notification_date or not message.tg_chat_id:
            continue

        try:
            print('Отправка: {0}'.format(message.message))
            tg_send(message.message, message.tg_chat_id)
            message.sent_date = current_datetime
            print('Записываю датувремя отправки')
            message.save()
        except Exception as e:
            message.error = str(e)
            message.save()
            print('Фэйл отправки')
            print(e)
    print('{0} Воркер send завершил свою работу'.format(str(datetime.now(tz=pytz.timezone('Asia/Krasnoyarsk')))))


if __name__ == '__main__':
    while True:
        check_new_message_task()
        sleep(30)

