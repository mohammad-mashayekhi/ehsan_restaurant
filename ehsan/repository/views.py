from django.shortcuts import render , redirect
from .models import Repository
from .forms import RepositoryForm
from datetime import datetime
from foodstuff.models import Stuffs,Category

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
        print(initial_form_data)
        form = RepositoryForm(initial=initial_form_data)  # استفاده از یک دیکشنری برای ارسال به عنوان initial
    
    categories = Category.objects.all()  # اضافه کردن دسته بندی‌ها
    stuffs = Stuffs.objects.select_related('stuff_category').all()
    return render(request, 'repository/in_repository.html', {'form': form, 'date': date, 'stuffs': stuffs, 'categories': categories})

def out_repository(request, date):
    gregorian_date = datetime.strptime(date, '%Y-%m-%d').date()  # تبدیل تاریخ به فرمت میلادی
    initial_type = 'out'

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
        form = RepositoryForm(initial=initial_form_data)  # استفاده از یک دیکشنری برای ارسال به عنوان initial
    
    categories = Category.objects.all()  # اضافه کردن دسته بندی‌ها
    stuffs = Stuffs.objects.select_related('stuff_category').all()
    return render(request, 'repository/out_repository.html', {'form': form, 'date': date, 'stuffs': stuffs, 'categories': categories})
