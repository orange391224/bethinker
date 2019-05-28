from django.db import models
from django.dispatch import receiver
from bethink.models.card import Card
from django.db.models.signals import post_save, post_delete


class TgMessage(models.Model):
    card_id = models.IntegerField()
    message = models.TextField()
    notification_date = models.DateTimeField(null=True)
    sent_date = models.DateTimeField(null=True, blank=True)
    tg_chat_id = models.CharField(max_length=30, blank=True, null=True)
    error = models.TextField(null=True,blank=True)


@receiver(post_save, sender=Card)
def create_message(sender, instance, created, **kwargs):
    if created:
        TgMessage.objects.create(card_id=instance.pk,
                                 message='{0} \n {1}'.format(instance.title, instance.body),
                                 notification_date=instance.notification_date)


@receiver(post_save, sender=Card)
def save_message(sender, instance, **kwargs):
    """
    message, created = TgMessage.objects.get_or_create(card_id=instance.pk)
    message.message = '{0} \n {1}'.format(instance.title, instance.body)
    message.notification_date = instance.notification_date
    message.save()
    #TgMessage.profile.save()

    message, created = TgMessage.objects.update_or_create(card_id=instance.pk,
                                                          message='{0} \n {1}'.format(instance.title, instance.body),
                                                          notification_date=instance.notification_date,
                                                          tg_chat_id=instance.user.profile.tg_id)
    #message.save()
    t=1
    """
    message, created = TgMessage.objects.get_or_create(card_id=instance.pk)
    message.notification_date = instance.notification_date
    message.message = '{0} \n {1}'.format(instance.title, instance.body)
    message.tg_chat_id = instance.user.profile.tg_id
    if message.sent_date:
        message.sent_date = None
    message.save()


@receiver(post_delete, sender=Card)
def del_message(sender, instance, **kwargs):
    message = TgMessage.objects.filter(card_id=instance.pk)
    if message:
        message[0].delete()
