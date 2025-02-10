from django import forms
from .models import Report
from datetime import date


class ReportForm(forms.ModelForm):
    year = forms.IntegerField(label="Год", initial=date.today().year, min_value=1900, max_value=date.today().year)
    month = forms.ChoiceField(
        label="Месяц",
        choices=[(i, month) for i, month in enumerate([
            "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
            "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
        ], start=1)]
    )

    class Meta:
        model = Report
        fields = ['year', 'month']
