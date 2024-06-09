from django.shortcuts import render, redirect, get_object_or_404
from .forms import RecipeForm, IngredientForm
from .models import Recipe
from django.forms import formset_factory
from foodstuff.models import Category, Stuffs, Price # وارد کردن مدل‌های Category و Stuffs
from django.db.models import F

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


def edit_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
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
    
import json
def recipe_list(request):
    recipes = Recipe.objects.all()
    prices_list = []

    # خواندن آخرین رکورد قیمت برای هر ماده اولیه و ایجاد یک دیکشنری
    latest_price_record = Price.objects.latest('date')
    latest_prices = latest_price_record.prices    
    
    for recipe in recipes:
        total_price = 0
        ingredients = recipe.ingredients
        
        # تبدیل رشته JSON به دیکشنری در صورت لزوم
        if isinstance(ingredients, str):
            ingredients = json.loads(ingredients)

        for stuff_id, quantity in ingredients.items():
            # بدست آوردن قیمت ماده اولیه از دیکشنری قیمت‌ها
            ingredient_price = float(latest_prices.get(stuff_id, 0))

            # محاسبه قیمت هر ماده اولیه با توجه به تعداد مورد استفاده
            total_price += quantity * ingredient_price
        
        # اضافه کردن اطلاعات به لیست
        prices_list.append({
            'recipe_id': recipe.recipe_id,
            'id': recipe.id,            
            'name': recipe.name,
            'total_price': total_price
        })

    return render(request, 'recipe/recipe_list.html', {'prices_list': prices_list})