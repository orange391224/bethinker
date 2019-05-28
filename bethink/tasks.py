from logging import getLogger
from background_task import background
# logger = getLogger(__name__)
from bethink.models.card import Card
from bethink.models.tgmessage import TgMessage
from datetime import datetime
import pytz

from bethink.utils import tg_send

"""
@background()
def notify_worker():
    # logger.debug('demo_task. message={0}'.format('test'))
    cards = Card.objects.all()
    for card in cards:
        if not card.notification_date:
            continue
        current_datetime = datetime.now(tz=pytz.timezone('Asia/Krasnoyarsk'))
        if current_datetime > card.notification_date:
            # проверим есть ли уже созаднный месседж
            message = TgMessage.objects.filter(card_id=card.pk)
            if message:
                print('Сообщение уже есть')
                continue
            # создание сообщения
            message = TgMessage.objects.create(card_id=card.pk,
                                               notification_date=card.notification_date)
            print('Сообщение {0} создано'.format(message.id))
    print('Воркер notify завершил свою работу')
"""
def reg_sent_tg_task():
    sent_tg_task(repeat=25)

@background()
def sent_tg_task():
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


def sent_tg_task_debug():
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
