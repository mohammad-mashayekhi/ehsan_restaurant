from django import forms
from accounting.models import DailyReport

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class DailyReportForm(forms.ModelForm):
    class Meta:
        model = DailyReport
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
