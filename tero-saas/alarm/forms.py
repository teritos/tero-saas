from django import forms

from alarm.models import AlarmImage


class AlarmImageForm(forms.ModelForm):
    
    class Meta:
        model = AlarmImage
        fields = ['image']