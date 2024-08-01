from datetime import datetime
from django.shortcuts import render, redirect, HttpResponse,get_object_or_404
from .models import MonthlyReport,ClaimDebt
from .forms import DailyReportForm ,ClaimsDebtsForm
from foodstuff.models import Category
from recipe.models import Recipe, RecipeSaleFile
from repository.models import Repository
from foodstuff.models import Stuffs , Price
import jdatetime
from collections import defaultdict
import json
from khayyam import JalaliDate


def report(request, date):
    date_object = datetime.strptime(date, '%Y-%m-%d').replace(day=1)
    jalali_date = jdatetime.date.fromgregorian(date=date_object).strftime('%Y/%m/%d')
    report_date = date_object.replace(day=1)

    # Get or create MonthlyReport instance for the given date
    report_instance, created = MonthlyReport.objects.get_or_create(date=report_date)

    if request.method == 'POST':
        form = DailyReportForm(request.POST, instance=report_instance)
        if form.is_valid():
            form.save()
            return render(request, 'record/report.html', {
                'form': form,
                'jalali_date': jalali_date,
                'date': date,
                'months': get_jalali_months(),
                'current_month': date  # Add the current month
            })
    else:
        form = DailyReportForm(instance=report_instance)

    return render(request, 'record/report.html', {
        'form': form,
        'jalali_date': jalali_date,
        'date': date,
        'months': get_jalali_months(),
        'current_month': date  # Add the current month
    })


def add_claimsdebts(request, date):
    date_object = datetime.strptime(date, '%Y-%m-%d').replace(day=1)
    jalali_date = jdatetime.date.fromgregorian(date=date_object).strftime('%Y/%m/%d')
    report_date = date_object.replace(day=1)

    # Get or create ClaimDebt instance for the given date
    report_instance, created = ClaimDebt.objects.get_or_create(date=report_date)

    if request.method == 'POST':
        form = ClaimsDebtsForm(request.POST, instance=report_instance)
        if form.is_valid():
            # Calculate total debts and claims
            total_claims = (
                form.cleaned_data['personal'] +
                form.cleaned_data['company'] +
                form.cleaned_data['specific_company']
            )
            total_debts = (
                form.cleaned_data['market'] +
                form.cleaned_data['meat'] +
                form.cleaned_data['other'] +
                form.cleaned_data['staff']
            )

            # Calculate balance and update the form instance
            x1 =  total_claims + form.cleaned_data['balance']
            x2 =  total_debts + form.cleaned_data['value_added_debt']
            form.instance.level = x1 - x2
            form.instance.total_claims = total_claims
            form.instance.total_debts = total_debts

            form.save()
            return redirect('record:claimsdebts', date=date)  # Redirect to the same view with the same date
    else:
        form = ClaimsDebtsForm(instance=report_instance)

    return render(request, 'record/claimsdebts.html', {
        'form': form,
        'jalali_date': jalali_date,
        'date': date,
        'months': get_jalali_months(),
        'current_month': date  # Add the current month
    })

# from django.forms import formset_factory
# from .forms import IngredientForm
# from .models import ClaimDebt
# def add_claimsdebts(request, date):
#     gregorian_date = datetime.strptime(date, '%Y-%m-%d')
#     jalali_date = jdatetime.date.fromgregorian(date=gregorian_date).strftime('%Y/%m/%d')

#     try:
#         date_obj = datetime.strptime(date, '%Y-%m-%d').date()
#     except ValueError:
#         return HttpResponse('Invalid date format', status=400)

#     if 0 <= date_obj.day <= 15:
#         creation_date = date_obj.replace(day=15)
#     else:
#         creation_date = date_obj.replace(day=30)

#     IngredientFormSet = formset_factory(IngredientForm, extra=1)

#     try:
#         claims = ClaimsDebts.objects.get(date_created=creation_date, type=ClaimsDebts.CLAIM)
#     except ClaimsDebts.DoesNotExist:
#         claims = ClaimsDebts(date_created=creation_date, type=ClaimsDebts.CLAIM)

#     try:
#         debts = ClaimsDebts.objects.get(date_created=creation_date, type=ClaimsDebts.DEBT)
#     except ClaimsDebts.DoesNotExist:
#         debts = ClaimsDebts(date_created=creation_date, type=ClaimsDebts.DEBT)

#     if request.method == 'POST':
#         claims_form = ClaimsForm(request.POST, instance=claims, prefix='claims')
#         debts_form = DebtsForm(request.POST, instance=debts, prefix='debts')
#         claims_formset = IngredientFormSet(request.POST, prefix='claims_ingredients')
#         debts_formset = IngredientFormSet(request.POST, prefix='debts_ingredients')
        
#         if claims_form.is_valid() and debts_form.is_valid() and claims_formset.is_valid() and debts_formset.is_valid():
#             claims = claims_form.save(commit=False)
#             debts = debts_form.save(commit=False)
            
#             claims.type = ClaimsDebts.CLAIM
#             debts.type = ClaimsDebts.DEBT
            
#             claims.date_created = creation_date
#             debts.date_created = creation_date
            
#             claims.save()
#             debts.save()
            
#             claims_ingredients = {form.cleaned_data.get('name'): form.cleaned_data.get('amount') for form in claims_formset
#                       if form.cleaned_data.get('name') and form.cleaned_data.get('amount') is not None}
#             debts_ingredients = {form.cleaned_data.get('name'): form.cleaned_data.get('amount') for form in debts_formset
#                       if form.cleaned_data.get('name') and form.cleaned_data.get('amount') is not None}
            
#             claims.ingredients = claims_ingredients
#             debts.ingredients = debts_ingredients
            
#             claims.save()
#             debts.save()
            
#             return redirect('record:claimsdebts', date=date)
#     else:
#         claims_form = ClaimsForm(instance=claims, prefix='claims')
#         debts_form = DebtsForm(instance=debts, prefix='debts')
        
#         if claims.id:
#             initial_data = [{'name': ingredient, 'amount': claims.ingredients.get(ingredient, 0)} for ingredient in claims.ingredients.keys()]
#             claims_formset = IngredientFormSet(initial=initial_data, prefix='claims_ingredients')
#         else:
#             claims_formset = IngredientFormSet(prefix='claims_ingredients')

#         if debts.id:
#             initial_data = [{'name': ingredient, 'amount': debts.ingredients.get(ingredient, 0)} for ingredient in debts.ingredients.keys()]
#             debts_formset = IngredientFormSet(initial=initial_data, prefix='debts_ingredients')
#         else:
#             debts_formset = IngredientFormSet(prefix='debts_ingredients')
        

#     return render(request, 'record/claimsdebts.html', {
#         'date': date,
#         'jalali_date': jalali_date,
#         'claims_form': claims_form,
#         'debts_form': debts_form,
#         'claims_formset': claims_formset,
#         'debts_formset': debts_formset,
#         'claims': claims,
#         'debts': debts,
#     })

def consumptionreport(request, date):
    gregorian_date = datetime.strptime(date, '%Y-%m-%d')
    jalali_date = jdatetime.date.fromgregorian(date=gregorian_date).strftime('%Y/%m/%d')
    
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        return HttpResponse('Invalid date format', status=400)

    # Retrieve all RecipeSaleFile records for the given date
    sales = RecipeSaleFile.objects.filter(date_created=date_obj)
    report_data = []
    # Retrieve the prices for the given date
    try:
        price_entry = Price.objects.get(date=date_obj)
        prices = price_entry.prices
    except Price.DoesNotExist:
        prices = {}

    total_recipe_amount = 0
    total_out_quantity = 0
    total_difference = 0
    total_percentage_difference = 0
    total_loss_amount = 0

    for sale in sales:
        # Parse recipe_prices JSON data
        recipe_prices = sale.recipe_prices

        for price in recipe_prices:
            recipe_id = price.get('code')
            
            recipe_id = str(recipe_id).zfill(8)

            count = price.get('count')
            print(recipe_id)
            # Retrieve the recipe based on recipe_id
            try:
                recipe = Recipe.objects.get(recipe_id=recipe_id)
            except Recipe.DoesNotExist:
                continue

            # Calculate total ingredients needed based on the sales quantity
            total_ingredients = {}
            for ingredient_id, quantity in recipe.ingredients.items():
                total_ingredients[ingredient_id] = quantity * count

            # Iterate over total_ingredients and prepare data for report_data
            for ingredient_id, amount in total_ingredients.items():
                ingredient = get_object_or_404(Stuffs, stuff_id=ingredient_id)
                ingredient_name = ingredient.stuff_name
                category_name = ingredient.stuff_category.cat_name

                # Initialize out_quantity as 0
                out_quantity = 0

                # Retrieve the repository out entries for the ingredient on the given date
                out_entries = Repository.objects.filter(date=date_obj, type='out')
                for entry in out_entries:
                    out_quantity += int(entry.quantities.get(str(ingredient_id), 0))

                # Calculate the difference and percentage difference
                difference = out_quantity - amount
                percentage_difference = (difference / amount) * 100 if amount != 0 else 0

                # Retrieve the price for the ingredient and convert to float
                price_per_unit = float(prices.get(str(ingredient_id), 0))
                loss_amount = difference * price_per_unit

                # Aggregate totals
                total_recipe_amount += amount
                total_out_quantity += out_quantity
                total_difference += difference
                total_loss_amount += loss_amount
                # Check if ingredient_name already exists in report_data
                found = False
                for item in report_data:
                    if item['ingredient_name'] == ingredient_name:
                        item['amount'] += amount
                        item['out_quantity'] += out_quantity
                        item['difference'] += difference
                        item['loss_amount'] += loss_amount
                        item['percentage_difference'] = (item['difference'] / item['amount']) * 100 if item['amount'] != 0 else 0
                        found = True
                        break

                if not found:
                    # Add new entry for the ingredient
                    report_data.append({
                        'ingredient_name': ingredient_name,
                        'category_name': category_name,
                        'amount': amount,
                        'out_quantity': out_quantity,
                        'difference': difference,
                        'percentage_difference': percentage_difference,
                        'loss_amount': loss_amount,
                    })

    # Calculate total percentage difference
    total_percentage_difference = (total_difference / total_recipe_amount) * 100 if total_recipe_amount != 0 else 0
    categories = Category.objects.all().order_by('cat_id')  # اضافه کردن دسته بندی‌ها

    context = {
        'date': date,
        'jalali_date': jalali_date,
        'categories':categories,
        'date_obj': date_obj,
        'report_data': report_data,
        'total_recipe_amount': total_recipe_amount,
        'total_out_quantity': total_out_quantity,
        'total_difference': total_difference,
        'total_percentage_difference': total_percentage_difference,
        'total_loss_amount': total_loss_amount,
    }

    return render(request, 'record/consumptionreport.html', context)

def reportchart(request, date):
    gregorian_date = datetime.strptime(date, '%Y-%m-%d')
    jalali_date = jdatetime.date.fromgregorian(date=gregorian_date).strftime('%Y/%m/%d')
    
    # تبدیل تاریخ از رشته به آبجکت datetime و تنظیم به ابتدای ماه
    report_date = datetime.strptime(date, '%Y-%m-%d')
    report_date = report_date.replace(day=1)
    
    # پیدا کردن گزارش برای ماه و سال مورد نظر
    report = MonthlyReport.objects.filter(date=report_date).first()
    
    # در صورتی که گزارشی یافت نشد، یک گزارش خالی ایجاد می‌کنیم
    if not report:
        sales_report = {
            "sales_hall": 0.0,
            "sales_takeaway": 0.0,
            "sales_snappfood": 0.0,
            "sales_company": 0.0,
            "sales_special_company": 0.0,
            "sales_charity": 0.0,
            "sales_charity1": 0.0,
            "sales_misc": 0.0,
            "total_sales": 0.0,
        }
        expenses_report = {
            "rent": 0.0,
            "salaries": 0.0,
            "hall": 0.0,
            "raw_materials": 0.0,
            "consumables": 0.0,
            "maintenance": 0.0,
            "delivery": 0.0,
            "misc_expenses": 0.0,
            "total_expenses": 0.0,
        }
    else:
        sales_report = {
            "sales_hall": float(report.sales_hall),
            "sales_takeaway": float(report.sales_takeaway),
            "sales_snappfood": float(report.sales_snappfood),
            "sales_company": float(report.sales_company),
            "sales_special_company": float(report.sales_special_company),
            "sales_charity": float(report.sales_charity),
            "sales_charity1": float(report.sales_charity1),
            "sales_misc": float(report.sales_misc),
            "total_sales": float(report.total_sales),
        }
        expenses_report = {
            "rent": float(report.rent),
            "salaries": float(report.salaries),
            "hall": float(report.hall),
            "raw_materials": float(report.raw_materials),
            "consumables": float(report.consumables),
            "maintenance": float(report.maintenance),
            "delivery": float(report.delivery),
            "misc_expenses": float(report.misc_expenses),
            "total_expenses": float(report.total_expenses),
        }
    
   # محاسبه درصد برای فروش‌ها
    sales_keys = list(sales_report.keys())
    for key in sales_keys:
        if key != 'total_sales' and sales_report['total_sales'] > 0:
            sales_report[key + '_percent'] = (sales_report[key] / sales_report['total_sales']) * 100
        else:
            sales_report[key + '_percent'] = 0.0

    # محاسبه درصد برای هزینه‌ها
    expenses_keys = list(expenses_report.keys())
    for key in expenses_keys:
        if key != 'total_expenses' and expenses_report['total_expenses'] > 0:
            expenses_report[key + '_percent'] = (expenses_report[key] / expenses_report['total_expenses']) * 100
        else:
            expenses_report[key + '_percent'] = 0.0
    
    
    # //////////////////////////////////////////////////////////////////
    current_date = JalaliDate.today()
    current_year = current_date.year  # دریافت سال جاری شمسی

    # دریافت تمامی داده‌های فروش از مدل RecipeSaleFile
    sales_data = RecipeSaleFile.objects.all()

    # آماده‌سازی defaultdict برای ذخیره‌سازی داده‌های فروش تجمیع شده
    monthly_sales = defaultdict(lambda: {'count': 0, 'total_price': 0})

    # تجمیع داده‌های فروش بر اساس ماه و سال
    for sale in sales_data:
        # تبدیل تاریخ میلادی به شمسی
        jalali_date = JalaliDate(sale.date_created)
        month = jalali_date.month
        year = jalali_date.year

        total_count = sum(item['count'] for item in sale.recipe_prices)
        total_price = sum(item['total_price'] for item in sale.recipe_prices)

        if year == current_year:  # در نظر گرفتن داده‌های سال جاری
            monthly_sales[month]['count'] += total_count
            monthly_sales[month]['total_price'] += total_price

    # تبدیل سال شمسی به میلادی برای فیلتر کردن در مدل MonthlyReport
    start_of_year_gregorian = JalaliDate(current_year, 1, 1).todate()
    end_of_year_gregorian = JalaliDate(current_year, 12, 29).todate()
    print(start_of_year_gregorian)
    print(end_of_year_gregorian)
    # Query MonthlyReport for the current year and calculate monthly profit and misc expenses
    monthly_reports = MonthlyReport.objects.filter(date__range=(start_of_year_gregorian, end_of_year_gregorian))
    monthly_profits = defaultdict(lambda: 0.0)
    monthly_expenses = defaultdict(lambda: 0.0)

    for report in monthly_reports:
        jalali_date = JalaliDate(report.date)
        month = jalali_date.month
        monthly_profits[month] += float(report.monthly_profit)
        monthly_expenses[month] += float(report.total_expenses)  # Assuming misc_expenses is a float field
        print(monthly_expenses)
    # آماده‌سازی داده‌ها برای نمودارها
    months = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']
    count_data = [monthly_sales[i]['count'] for i in range(1, 13)]
    price_data = [monthly_sales[i]['total_price'] / 1000000.0 for i in range(1, 13)]  # تقسیم بر ۱۰۰۰۰۰۰ و تبدیل به float
    profit_data = [monthly_profits[i] for i in range(1, 13)]
    expense_data = [monthly_expenses[i] for i in range(1, 13)]

    # آماده‌سازی داده‌ها به صورت دیکشنری
    data_dict = {}
    for i in range(12):
        data_dict[f'count{i+1}'] = count_data[i]
        data_dict[f'price{i+1}'] = price_data[i]
        data_dict[f'profit{i+1}'] = profit_data[i]
        data_dict[f'expense{i+1}'] = expense_data[i]

    # تبدیل داده‌ها به فرمت JSON
    chart_data_json = json.dumps(data_dict)
    
    
    return render(request, 'record/report-chart.html', {
        'chart_data_json': chart_data_json,
        'chart_data_year': current_year,
        'sales_report': sales_report,
        'expenses_report': expenses_report,
        'jalali_date': jalali_date,
        'date': date,
        'months': get_jalali_months(),
    })

def monthsale(request, date):
    current_date = JalaliDate.today()
    current_year = current_date.year  # دریافت سال جاری شمسی

    # دریافت تمامی داده‌های فروش از مدل RecipeSaleFile
    sales_data = RecipeSaleFile.objects.all()

    # آماده‌سازی defaultdict برای ذخیره‌سازی داده‌های فروش تجمیع شده
    monthly_sales = defaultdict(lambda: {'count': 0, 'total_price': 0})

    # تجمیع داده‌های فروش بر اساس ماه و سال
    for sale in sales_data:
        # تبدیل تاریخ میلادی به شمسی
        jalali_date = JalaliDate(sale.date_created)
        month = jalali_date.month
        year = jalali_date.year

        total_count = sum(item['count'] for item in sale.recipe_prices)
        total_price = sum(item['total_price'] for item in sale.recipe_prices)

        if year == current_year:  # در نظر گرفتن داده‌های سال جاری
            monthly_sales[month]['count'] += total_count
            monthly_sales[month]['total_price'] += total_price

    # تبدیل سال شمسی به میلادی برای فیلتر کردن در مدل MonthlyReport
    start_of_year_gregorian = JalaliDate(current_year, 1, 1).todate()
    end_of_year_gregorian = JalaliDate(current_year, 12, 29).todate()
    print(start_of_year_gregorian)
    print(end_of_year_gregorian)
    # Query MonthlyReport for the current year and calculate monthly profit and misc expenses
    monthly_reports = MonthlyReport.objects.filter(date__range=(start_of_year_gregorian, end_of_year_gregorian))
    monthly_profits = defaultdict(lambda: 0.0)
    monthly_expenses = defaultdict(lambda: 0.0)

    for report in monthly_reports:
        jalali_date = JalaliDate(report.date)
        month = jalali_date.month
        monthly_profits[month] += float(report.monthly_profit)
        monthly_expenses[month] += float(report.total_expenses)  # Assuming misc_expenses is a float field
        print(monthly_expenses)
    # آماده‌سازی داده‌ها برای نمودارها
    months = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']
    count_data = [monthly_sales[i]['count'] for i in range(1, 13)]
    price_data = [monthly_sales[i]['total_price'] / 1000000.0 for i in range(1, 13)]  # تقسیم بر ۱۰۰۰۰۰۰ و تبدیل به float
    profit_data = [monthly_profits[i] for i in range(1, 13)]
    expense_data = [monthly_expenses[i] for i in range(1, 13)]

    # آماده‌سازی داده‌ها به صورت دیکشنری
    data_dict = {}
    for i in range(12):
        data_dict[f'count{i+1}'] = count_data[i]
        data_dict[f'price{i+1}'] = price_data[i]
        data_dict[f'profit{i+1}'] = profit_data[i]
        data_dict[f'expense{i+1}'] = expense_data[i]

    # تبدیل داده‌ها به فرمت JSON
    chart_data_json = json.dumps(data_dict)

    context = {
        'chart_data_json': chart_data_json,
        'chart_data_year': current_year,
    }

    return render(request, 'record/report-monthsale.html', context)

def get_jalali_months():
    """ 
    Generates a list of dictionaries for each month of the current year.
    Each dictionary contains the month name and corresponding URL date.
    """
    # Define Persian names for Jalali months
    jalali_month_names = {
        1: 'فروردین',
        2: 'اردیبهشت',
        3: 'خرداد',
        4: 'تیر',
        5: 'مرداد',
        6: 'شهریور',
        7: 'مهر',
        8: 'آبان',
        9: 'آذر',
        10: 'دی',
        11: 'بهمن',
        12: 'اسفند'
    }

    year = jdatetime.date.today().year
    months = []

    for month in range(1, 13):
        # Create a Jalali date object
        jalali_date = jdatetime.date(year, month, 1)
        # Convert Jalali date to Gregorian date
        gregorian_date = jalali_date.togregorian()
        # Format the Gregorian date to 'YYYY-MM-DD'
        formatted_date = gregorian_date.strftime('%Y-%m-%d')
        # Get the month name in Persian
        month_name = jalali_month_names[month]
        months.append({
            'name': month_name,
            'url_date': formatted_date
        })

    return months