from datetime import datetime
from django.shortcuts import render, redirect
from .models import MonthlyReport
from .forms import DailyReportForm ,IngredientForm

def report(request, date):
    date_object = datetime.strptime(date, '%Y-%m-%d').replace(day=1)

    # Get or create MonthlyReport instance for the given date
    report_instance, created = MonthlyReport.objects.get_or_create(date=date_object)

    if request.method == 'POST':
        form = DailyReportForm(request.POST, instance=report_instance)
        if form.is_valid():
            form.save()
            return render(request, 'record/report.html', {
                'form': form,
                'date': date,
            })
    else:
        form = DailyReportForm(instance=report_instance)

    return render(request, 'record/report.html', {
        'form': form,
        'date': date,
    })


from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.forms import formset_factory
from .forms import ClaimsForm, DebtsForm, IngredientForm
from .models import ClaimsDebts

def add_claimsdebts(request, date):
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        return HttpResponse('Invalid date format', status=400)

    if 0 <= date_obj.day <= 15:
        creation_date = date_obj.replace(day=15)
    else:
        creation_date = date_obj.replace(day=30)

    IngredientFormSet = formset_factory(IngredientForm, extra=1)

    try:
        claims = ClaimsDebts.objects.get(date_created=creation_date, type=ClaimsDebts.CLAIM)
    except ClaimsDebts.DoesNotExist:
        claims = ClaimsDebts(date_created=creation_date, type=ClaimsDebts.CLAIM)

    try:
        debts = ClaimsDebts.objects.get(date_created=creation_date, type=ClaimsDebts.DEBT)
    except ClaimsDebts.DoesNotExist:
        debts = ClaimsDebts(date_created=creation_date, type=ClaimsDebts.DEBT)

    if request.method == 'POST':
        claims_form = ClaimsForm(request.POST, instance=claims, prefix='claims')
        debts_form = DebtsForm(request.POST, instance=debts, prefix='debts')
        claims_formset = IngredientFormSet(request.POST, prefix='claims_ingredients')
        debts_formset = IngredientFormSet(request.POST, prefix='debts_ingredients')
        
        if claims_form.is_valid() and debts_form.is_valid() and claims_formset.is_valid() and debts_formset.is_valid():
            claims = claims_form.save(commit=False)
            debts = debts_form.save(commit=False)
            
            claims.type = ClaimsDebts.CLAIM
            debts.type = ClaimsDebts.DEBT
            
            claims.date_created = creation_date
            debts.date_created = creation_date
            
            claims.save()
            debts.save()
            
            claims_ingredients = {form.cleaned_data.get('name'): form.cleaned_data.get('amount') for form in claims_formset
                      if form.cleaned_data.get('name') and form.cleaned_data.get('amount') is not None}
            debts_ingredients = {form.cleaned_data.get('name'): form.cleaned_data.get('amount') for form in debts_formset
                      if form.cleaned_data.get('name') and form.cleaned_data.get('amount') is not None}
            
            claims.ingredients = claims_ingredients
            debts.ingredients = debts_ingredients
            
            claims.save()
            debts.save()
            
            return redirect('record:claimsdebts', date=date)
    else:
        claims_form = ClaimsForm(instance=claims, prefix='claims')
        debts_form = DebtsForm(instance=debts, prefix='debts')
        
        if claims.id:
            initial_data = [{'name': ingredient, 'amount': claims.ingredients.get(ingredient, 0)} for ingredient in claims.ingredients.keys()]
            claims_formset = IngredientFormSet(initial=initial_data, prefix='claims_ingredients')
        else:
            claims_formset = IngredientFormSet(prefix='claims_ingredients')

        if debts.id:
            initial_data = [{'name': ingredient, 'amount': debts.ingredients.get(ingredient, 0)} for ingredient in debts.ingredients.keys()]
            debts_formset = IngredientFormSet(initial=initial_data, prefix='debts_ingredients')
        else:
            debts_formset = IngredientFormSet(prefix='debts_ingredients')
        

    return render(request, 'record/claimsdebts.html', {
        'date': date,
        'claims_form': claims_form,
        'debts_form': debts_form,
        'claims_formset': claims_formset,
        'debts_formset': debts_formset,
        'claims': claims,
        'debts': debts,
    })

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from recipe.models import Recipe, RecipeSaleFile
from datetime import datetime
from django.db.models import Sum
from foodstuff.models import Stuffs

from django.shortcuts import render, HttpResponse
from django.utils import timezone
from datetime import datetime
from recipe.models import Recipe, RecipeSaleFile

def consumptionreport(request, date):
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        return HttpResponse('Invalid date format', status=400)

    # Retrieve all RecipeSaleFile records for the given date
    sales = RecipeSaleFile.objects.filter(created_at=date_obj)
    report_data = []

    for sale in sales:
        # Parse recipe_prices JSON data
        recipe_prices = sale.recipe_prices
        for price in recipe_prices:
            recipe_id = price.get('code')
            count = price.get('count')

            # Retrieve the recipe based on recipe_id
            try:
                recipe = Recipe.objects.get(recipe_id=recipe_id)
            except Recipe.DoesNotExist:
                continue
        
            # Calculate total ingredients needed based on the sales quantity
            total_ingredients = {}
            for ingredient_name, quantity in recipe.ingredients.items():
                total_ingredients[ingredient_name] = quantity * count

            # Iterate over total_ingredients and prepare data for report_data
            for ingredient_name, amount in total_ingredients.items():
                # Check if ingredient_name already exists in report_data
                found = False
                for item in report_data:
                    if item['ingredient_name'] == ingredient_name:
                        item['amount'] += amount
                        found = True
                        break
                
                if not found:
                    # Add new entry for the ingredient
                    report_data.append({
                        'ingredient_name': ingredient_name,
                        'amount': amount,
                    })

    context = {
        'date': date_obj,
        'report_data': report_data,
    }

    return render(request, 'record/consumptionreport.html', context)
