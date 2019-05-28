from django import forms
from bethink.models.profile import Profile
from bootstrap_datepicker_plus import DatePickerInput


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = {'tg_id', 'birth_date'}
        labels = {'tg_id': 'ID чата',
                  'birth_date': 'Дата рождения'}
        widgets = {'birth_date': DatePickerInput(format='%Y-%m-%d',
                                                 options={'locale': 'ru'})
                   }
