from django.shortcuts import render, redirect, get_object_or_404
from .forms import RecipeForm, IngredientForm
from .models import Recipe
from django.forms import formset_factory
from foodstuff.models import Category, Stuffs  # وارد کردن مدل‌های Category و Stuffs

def add_recipe(request):
    IngredientFormSet = formset_factory(IngredientForm, extra=1)
    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST)
        formset = IngredientFormSet(request.POST, prefix='ingredients')
        if recipe_form.is_valid() and formset.is_valid():
            recipe = recipe_form.save(commit=False)
            ingredients = {form.cleaned_data['stuff_name'].stuff_id: form.cleaned_data['amount'] for form in formset}
            recipe.ingredients = ingredients
            recipe.save()
            return redirect('recipe:recipe_list')
    else:
        recipe_form = RecipeForm()
        formset = IngredientFormSet(prefix='ingredients')

    # اضافه کردن دسته‌بندی‌ها برای نمایش در قالب
    categories = Category.objects.all()

    return render(request, 'recipe/add_recipe.html', {
        'recipe_form': recipe_form,
        'formset': formset,
        'categories': categories,  # ارسال دسته‌بندی‌ها به قالب
    })


def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    IngredientFormSet = formset_factory(IngredientForm, extra=0)
    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST, instance=recipe)
        formset = IngredientFormSet(request.POST, prefix='ingredients')
        if recipe_form.is_valid() and formset.is_valid():
            recipe = recipe_form.save(commit=False)
            ingredients = {form.cleaned_data['stuff_name'].stuff_id: form.cleaned_data['amount'] for form in formset}
            recipe.ingredients = ingredients
            recipe.save()
            return redirect('recipe:recipe_list')
    else:
        recipe_form = RecipeForm(instance=recipe)
        initial_data = [{'stuff_name': Stuffs.objects.get(stuff_id=stuff_id), 'amount': amount} for stuff_id, amount in recipe.ingredients.items()]
        formset = IngredientFormSet(initial=initial_data, prefix='ingredients')

    # اضافه کردن دسته‌بندی‌ها برای نمایش در قالب
    categories = Category.objects.all()

    return render(request, 'recipe/edit_recipe.html', {
        'recipe_form': recipe_form,
        'formset': formset,
        'categories': categories,  # ارسال دسته‌بندی‌ها به قالب
    })


def recipe_list(request):
    recipes = Recipe.objects.all()
    ingredients_dict = {}
    print(ingredients_dict)
    return render(request, 'recipe/recipe_list.html', {'recipes': recipes, 'ingredients_dict': ingredients_dict})
