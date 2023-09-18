from django import forms
from django.forms.widgets import DateInput


class StockDetailsForm(forms.Form):
    symbol = forms.CharField(label='Symbol', max_length=100)
    time_from = forms.DateField(
        label='Time From', widget=DateInput(attrs={'type': 'date'}))
    time_to = forms.DateField(
        label='Time To', widget=DateInput(attrs={'type': 'date'}))

    DAY_CHOICES = [
        ("D", "Day"),
        ("1", "1 minute"),
        ("2", "2 minutes"),
        ("3", "3 minutes"),
        ("5", "5 minutes"),
        ("10", "10 minutes"),
        ("15", "15 minutes"),
        ("20", "20 minutes"),
        ("30", "30 minutes"),
        ("60", "60 minutes"),
        ("120", "120 minutes"),
        ("240", "240 minutes"),
    ]

    time_period = forms.ChoiceField(choices=DAY_CHOICES, label='Day/Minute')
