from django.shortcuts import render, redirect, get_object_or_404
from .forms import RecipeForm, IngredientForm
from .models import Recipe,RecipePrice
from django.forms import formset_factory
from foodstuff.models import Category, Stuffs, Price # وارد کردن مدل‌های Category و Stuffs
from django.db.models import F
from django.http import JsonResponse
import json
import jdatetime
from datetime import datetime

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
        try:
            recipe_prices_data = RecipePrice.objects.latest('created_at')
            jalali_standard_price_data = jdatetime.date.fromgregorian(date=recipe_prices_data.created_at).strftime('%Y/%m/%d')
            percentage_difference = ((total_price - get_standard_price(recipe.id)) / get_standard_price(recipe.id)) * 100 if get_standard_price(recipe.id) else 0
        except:
            jalali_standard_price_data =''
            percentage_difference = ''
            
        jalali_price_date = jdatetime.date.fromgregorian(date=latest_price_record.date).strftime('%Y/%m/%d')

        # اضافه کردن اطلاعات به لیست
        prices_list.append({
            'recipe_id': recipe.recipe_id,
            'id': recipe.id,            
            'name': recipe.name,
            'total_price': total_price,
            'standard_price': get_standard_price(recipe.id),  # اضافه کردن قیمت معیار
            'percentage_difference': percentage_difference,
        })

    return render(request, 'recipe/recipe_list.html', {'prices_list': prices_list,'jalali_price_date': jalali_price_date,'jalali_standard_price_data': jalali_standard_price_data,})

def get_standard_price(recipe_id):
    # اینجا قیمت معیار را از مدل RecipePrice بر اساس recipe_id بخوانید و برگردانید
    try:
        recipe_prices_data = RecipePrice.objects.latest('created_at').recipe_prices
        recipe_prices_dict = json.loads(recipe_prices_data)
        for recipe_price in recipe_prices_dict:
            if recipe_price['id'] == recipe_id:
                return recipe_price['total_price']
        return ''
    except RecipePrice.DoesNotExist:
        return ''
    
def save_recipe_prices_ajax(request):
    recipe_prices_data = request.POST.get('recipe_prices')
    print(recipe_prices_data)
    RecipePrice.objects.create(recipe_prices=recipe_prices_data)
    return JsonResponse({'success': True})


from .forms import RecipeSearchForm
# views.py
from django.http import JsonResponse

def recipe_selection(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = RecipeSearchForm(request.POST)
        if form.is_valid():
            recipe_id = form.cleaned_data['recipe_id']
            quantity = form.cleaned_data['quantity']
            
            recipe = Recipe.objects.get(recipe_id=recipe_id)
            ingredients = recipe.ingredients
            total_ingredients = {}

            for stuff_id, amount in ingredients.items():
                if stuff_id in total_ingredients:
                    total_ingredients[stuff_id] += amount * quantity
                else:
                    total_ingredients[stuff_id] = amount * quantity

            ingredients_details = {Stuffs.objects.get(stuff_id=key).stuff_name: value for key, value in total_ingredients.items()}

            return JsonResponse({'success': True, 'recipe': recipe.name, 'quantity': quantity, 'ingredients_details': ingredients_details})

        return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = RecipeSearchForm()

    return render(request, 'recipe/recipe_selection.html', {'form': form})


import pandas as pd
from django.core.files.storage import FileSystemStorage
from .models import RecipeSaleFile
from .forms import UploadFileForm
from django.utils.timezone import now
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render, redirect
import numpy as np

def upload_file(request):
    today_date = datetime.today().strftime('%Y-%m-%d')
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            file_path = fs.path(filename)
            
            # خواندن فایل اکسل
            try:
                df = pd.read_excel(file_path, header=1)
                messages.success(request, 'فایل با موفقیت بارگذاری شد.')
            except Exception as e:
                form.add_error(None, f"Error reading Excel file: {str(e)}")
                return render(request, 'recipe/upload.html', {'form': form})

            # بررسی و به‌روزرسانی یا ایجاد رکورد جدید با اعتبارسنجی
            today = now().date()
            extracted_data = []
            for index, row in df.iterrows():
                if not pd.isnull(row['كد كالا']) and not pd.isnull(row['نام كالا']) and not pd.isnull(row['تعداد']):
                    item = {
                        'code': row['كد كالا'],
                        'product_name': row['نام كالا'],
                        'count': row['تعداد']
                    }
                    extracted_data.append(item)

            # بررسی اعتبارسنجی
            if not extracted_data:
                form.add_error(None, "هیچ داده معتبری در فایل یافت نشد.")
                return render(request, 'recipe/upload.html', {'form': form})

            # ذخیره یا به‌روزرسانی رکورد
            RecipeSaleFile.objects.update_or_create(
                created_at=today,
                defaults={'recipe_prices': extracted_data}
            )
            return redirect(reverse('recipe:salereport', kwargs={'date': today_date}))
    else:
        form = UploadFileForm()
    return render(request, 'recipe/upload.html', {'form': form})


from django.http import Http404
from django.utils.dateparse import parse_date

def salereport(request, date):
    try:
        # تلاش برای تبدیل رشته تاریخ به فرمت تاریخ
        parsed_date = parse_date(date)
        if not parsed_date:
            raise ValueError("Invalid date format")
        data = []
        # پیدا کردن فایل‌های بارگذاری شده در تاریخ مشخص شده
        file = RecipeSaleFile.objects.get(created_at=parsed_date)
        print(file.recipe_prices)
       
        context = {
            'file': file,
            'date': date,
        }
        return render(request, 'recipe/salereport.html', context)
        
    except RecipeSaleFile.DoesNotExist:
        context = {
            'date': date,
        }
        return render(request, 'recipe/salereport.html', context)
    except ValueError:
        raise Http404("Invalid date format. Please use YYYY-MM-DD.")