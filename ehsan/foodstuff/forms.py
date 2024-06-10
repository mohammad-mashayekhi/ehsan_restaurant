from django import forms
from .models import Stuffs, Category,Price

class StuffsForm(forms.ModelForm):
    class Meta:
        model = Stuffs
        fields = ['stuff_name', 'stuff_category', 'stuff_scale']
        widgets = {
            'stuff_name': forms.TextInput(attrs={'class': 'form-control'}),
            'stuff_category': forms.Select(attrs={'class': 'form-select'}),
            'stuff_scale': forms.Select(attrs={'class': 'form-select'}),
        }

class PriceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PriceForm, self).__init__(*args, **kwargs)
        stuffs = Stuffs.objects.all()
        for stuff in stuffs:
            self.fields[f'stuff_{stuff.stuff_id}'] = forms.CharField(
                label=stuff.stuff_name, required=False, widget=forms.TextInput(attrs={'class': 'price-input'})
            )
            
    def clean(self):
        cleaned_data = super(PriceForm, self).clean()
        prices = {}
        for field_name, value in cleaned_data.items():
            if field_name.startswith('stuff_'):
                stuff_id = field_name.split('_')[1]
                # Remove commas before saving to the database
                prices[stuff_id] = value.replace(',', '')
        cleaned_data['prices'] = prices
        return cleaned_data