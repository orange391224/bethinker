from django import forms
from bethink.models.card import Card
from bootstrap_datepicker_plus import DateTimePickerInput


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ('title', 'body', 'notification_date')
        localized_fields = ('notification_date',)
        labels = {'title': 'Заголовок',
                  'body': 'Текст',
                  'notification_date': 'Дата напоминания'}
        widgets = {'notification_date': DateTimePickerInput(format='%Y-%m-%d %H:%M',
                                                            options={'locale': 'ru'}
                                                            ),
                   'body': forms.Textarea(attrs={'cols': 40, 'rows': 5})
                   }
