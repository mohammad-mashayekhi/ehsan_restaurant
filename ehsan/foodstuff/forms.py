from django import forms
from .models import Stuffs, Category

class StuffsForm(forms.ModelForm):
    class Meta:
        model = Stuffs
        fields = ['stuff_name', 'stuff_category', 'stuff_scale']
       