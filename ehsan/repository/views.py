from django.shortcuts import render , redirect
from .models import Repository
from .forms import RepositoryForm
from datetime import datetime
from foodstuff.models import Stuffs,Category
import jdatetime

def repository(request):
    return render(request, 'repository/repository.html')


def in_repository(request, date):
    gregorian_date = datetime.strptime(date, '%Y-%m-%d').date()  # تبدیل تاریخ به فرمت میلادی
    initial_type = 'in'

    repository_instance = None
    initial_data = None  # تعیین مقدار اولیه برای initial_data
    all_stuff_ids = Stuffs.objects.values_list('stuff_id', flat=True)

    if Repository.objects.filter(date=gregorian_date, type='in').exists():  # بررسی وجود رکورد
            repository_instance = Repository.objects.get(date=gregorian_date, type='in')
            initial_data = {'type': initial_type, **{'stuff_' + str(stuff_id): quantity for stuff_id, quantity in repository_instance.quantities.items()}}
            
    if request.method == 'POST':
        form = RepositoryForm(request.POST, initial=initial_data)
        if form.is_valid():
            quantities = form.cleaned_data['quantities']
            type = initial_type
            if repository_instance:
                repository_instance.quantities = quantities
                repository_instance.type = type
                repository_instance.save()
            else:
                repository_instance = Repository.objects.create(date=gregorian_date, type=type, quantities=quantities)
            today_date = datetime.now().strftime('%Y-%m-%d')
            return redirect(f'/repository/in/{today_date}/')
    else:
        initial_form_data = {'date': gregorian_date, 'type': initial_type}
        if initial_data:
            initial_form_data.update(initial_data)  # فقط اگر initial_data موجود باشد، آن را به initial_form_data اضافه کنید
        else:
            initial_data = {'type': initial_type,**{'stuff_' + str(stuff_id): 0 for stuff_id in all_stuff_ids}}
            initial_form_data.update(initial_data)  # فقط اگر initial_data موجود باشد، آن را به initial_form_data اضافه کنید
        form = RepositoryForm(initial=initial_form_data)  # استفاده از یک دیکشنری برای ارسال به عنوان initial
    
    jalali_date = jdatetime.date.fromgregorian(date=gregorian_date).strftime('%Y/%m/%d')
    print(jalali_date)

    categories = Category.objects.all().order_by('cat_id')  # اضافه کردن دسته بندی‌ها
    stuffs = Stuffs.objects.select_related('stuff_category').all()
    return render(request, 'repository/in_repository.html', {'form': form,'jalali_date':jalali_date ,'date': date, 'stuffs': stuffs, 'categories': categories})

def out_repository(request, date):
    gregorian_date = datetime.strptime(date, '%Y-%m-%d').date()  # تبدیل تاریخ به فرمت میلادی
    initial_type = 'out'
    all_stuff_ids = Stuffs.objects.values_list('stuff_id', flat=True)

    repository_instance = None
    initial_data = None

    if Repository.objects.filter(date=gregorian_date, type='out').exists():
        try:
            repository_instance = Repository.objects.get(date=gregorian_date, type='out')
            initial_data = {'type': initial_type, **{'stuff_' + str(stuff_id): quantity for stuff_id, quantity in repository_instance.quantities.items()}}
        except Repository.DoesNotExist:
            pass

    if request.method == 'POST':
        form = RepositoryForm(request.POST, initial=initial_data)
        if form.is_valid():
            quantities = form.cleaned_data['quantities']
            type = initial_type
            if repository_instance:
                repository_instance.quantities = quantities
                repository_instance.type = type
                repository_instance.save()
            else:
                repository_instance = Repository.objects.create(date=gregorian_date, type=type, quantities=quantities)
            today_date = datetime.now().strftime('%Y-%m-%d')
            return redirect(f'/repository/out/{today_date}/')
    else:
        initial_form_data = {'date': gregorian_date, 'type': initial_type}
        if initial_data:
            initial_form_data.update(initial_data)  # فقط اگر initial_data موجود باشد، آن را به initial_form_data اضافه کنید
        else:
            initial_data = {'type': initial_type,**{'stuff_' + str(stuff_id): 0 for stuff_id in all_stuff_ids}}
            initial_form_data.update(initial_data)  # فقط اگر initial_data موجود باشد، آن را به initial_form_data اضافه کنید
        form = RepositoryForm(initial=initial_form_data)  # استفاده از یک دیکشنری برای ارسال به عنوان initial
        
    jalali_date = jdatetime.date.fromgregorian(date=gregorian_date).strftime('%Y/%m/%d')
    categories = Category.objects.all().order_by('cat_id')  # اضافه کردن دسته بندی‌ها
    stuffs = Stuffs.objects.select_related('stuff_category').all()
    return render(request, 'repository/out_repository.html', {'form': form,'jalali_date':jalali_date,'date': date, 'stuffs': stuffs, 'categories': categories})

from django.http import HttpResponse
from .models import Repository

from django.shortcuts import render
from .models import Repository

def TotalInventoryView(request):
    # Define dictionaries to store the sum of quantities for each stuff_id for 'in' and 'out' types
    quantities_sum_in = {}
    quantities_sum_out = {}
    categories = Category.objects.all()  # اضافه کردن دسته بندی‌ها

    # Get repositories with type 'in'
    repositories_in = Repository.objects.filter(type='in')
    
    # Get repositories with type 'out'
    repositories_out = Repository.objects.filter(type='out')
    
    # Function to accumulate quantities for each stuff_id
    def accumulate_quantities(repositories, quantities_sum):
        for repo in repositories:
            for stuff_id, quantity in repo.quantities.items():
                # Remove commas from the quantity string and then convert to integer
                quantity = quantity.replace(',', '')
                quantities_sum[stuff_id] = quantities_sum.get(stuff_id, 0) + int(quantity)
    
    # Accumulate quantities for 'in' type repositories
    accumulate_quantities(repositories_in, quantities_sum_in)
    
    # Accumulate quantities for 'out' type repositories
    accumulate_quantities(repositories_out, quantities_sum_out)
    
    # Calculate net sum of quantities for each stuff_id
    net_quantities = {}
    for stuff_id, sum_quantity_in in quantities_sum_in.items():
        sum_quantity_out = quantities_sum_out.get(stuff_id, 0)
        net_quantity = sum_quantity_in - sum_quantity_out
        net_quantities[stuff_id] = net_quantity

    # Prepare data for rendering
    data = []
    for stuff_id, net_quantity in net_quantities.items():
        sum_quantity_in = quantities_sum_in.get(stuff_id, 0)
        sum_quantity_out = quantities_sum_out.get(stuff_id, 0)
        # Get stuff_name from the database
        stuff_name = Stuffs.objects.get(stuff_id=stuff_id).stuff_name  # Assuming you have a model for stuff
        stuff_category = Stuffs.objects.get(stuff_id=stuff_id).stuff_category  # Assuming you have a model for stuff

        data.append({
            'stuff_id': stuff_id,
            'stuff_name': stuff_name,
            'stuff_category': stuff_category,
            'sum_quantity_in': sum_quantity_in,
            'sum_quantity_out': sum_quantity_out,
            'net_quantity': net_quantity
        })
    
    # Render the template with the data
    return render(request, 'repository/total_inventory.html', {'data': data, 'categories': categories})