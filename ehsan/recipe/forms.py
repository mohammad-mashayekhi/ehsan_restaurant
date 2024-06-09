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

class RecipeSearchForm(forms.Form):
    recipe_id = forms.ChoiceField(
        choices=[(recipe.recipe_id, recipe.name) for recipe in Recipe.objects.all()],
        label="انتخاب غذا",
        widget=forms.Select(attrs={'class': 'recipe-select'})
    )
    quantity = forms.IntegerField(
        label="تعداد",
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'recipe-quantity'})
    )