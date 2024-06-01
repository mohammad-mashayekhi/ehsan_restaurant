from django import forms
from foodstuff.models import Stuffs


class RepositoryForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(RepositoryForm, self).__init__(*args, **kwargs)
        stuffs = Stuffs.objects.all()
        for stuff in stuffs:
            self.fields[f'stuff_{stuff.stuff_id}'] = forms.IntegerField(label=stuff.stuff_name, required=False, min_value=0)

    def clean(self):
        cleaned_data = super(RepositoryForm, self).clean()
        quantities = {}
        for field_name, value in cleaned_data.items():
            if field_name.startswith('stuff_'):
                stuff_id = field_name.split('_')[1]
                quantities[stuff_id] = value
        cleaned_data['quantities'] = quantities
        return cleaned_data