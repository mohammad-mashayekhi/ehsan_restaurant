from django import forms
from .models import Recipe
from foodstuff.models import Stuffs

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['recipe_id', 'name']  # اضافه کردن recipe_id به فیلدها
        widgets = {
            'recipe_id': forms.TextInput(attrs={'class': 'form-control'}), 
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    labels = {
                'recipe_id': 'شناسه رسپی',
                'name': 'نام غذا',
            }
      
class IngredientForm(forms.Form):
    stuff_name = forms.ModelChoiceField(
        queryset=Stuffs.objects.all(),
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='نام ماده اولیه'
    )
    amount = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control mt-1', 'placeholder': 'مقدار'}),
        label='مقدار'
    )


class RecipeSelectionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(RecipeSelectionForm, self).__init__(*args, **kwargs)
        recipes = Recipe.objects.all()
        for recipe in recipes:
            self.fields[f'recipe_{recipe.recipe_id}'] = forms.IntegerField(
                label=recipe.name, required=False, min_value=0, widget=forms.NumberInput(attrs={'class': 'recipe-input'})
            )