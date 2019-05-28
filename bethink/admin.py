from django.contrib import admin

# Register your models here.
from bethink.models.card import Card
from bethink.models.profile import Profile
from bethink.models.tgmessage import TgMessage


class MessageAdmin(admin.ModelAdmin):
    list_display = ('card_id', 'message', 'notification_date', 'sent_date')
    list_display_links = ('card_id', 'message')
    search_fields = ('card_id', 'message')


admin.site.register(Card)
admin.site.register(Profile)
admin.site.register(TgMessage, MessageAdmin)
