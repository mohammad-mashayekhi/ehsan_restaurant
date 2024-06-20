from django.shortcuts import render, get_object_or_404, redirect
from .forms import StuffsForm ,PriceForm
from .models import Stuffs ,Category, Price
from django.utils import timezone
import jdatetime
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# def foodstuffs(request):
#     stuffs = Stuffs.objects.all()
#     last_price = Price.objects.latest('date')
#     last_price_jalali = jdatetime.date.fromgregorian(date=last_price.date).strftime('%Y/%m/%d')
#     return render(request, 'foodstuff/table-foodstuffs.html', {'stuffs': stuffs, 'last_price_jalali': last_price_jalali})

def addfoodstuffs(request):
    today_date = datetime.today().strftime('%Y-%m-%d')
    categories = Category.objects.all()
    if request.method == "POST":
        form = StuffsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('foodstuff:add_price', kwargs={'date': today_date}))
    else:
        form = StuffsForm()
    
    return render(request, 'foodstuff/add-foodstuffs.html', {'categories': categories,'form': form})

def edit_stuff(request, id):
    today_date = datetime.today().strftime('%Y-%m-%d')
    stuff = get_object_or_404(Stuffs, id=id)
    if request.method == "POST":
        form = StuffsForm(request.POST, instance=stuff)
        if form.is_valid():
            form.save()
            return redirect(reverse('foodstuff:add_price', kwargs={'date': today_date}))
    else:
        form = StuffsForm(instance=stuff)
    return render(request, 'foodstuff/edit_stuff.html', {'form': form ,'id':id})


from django.shortcuts import render, redirect
from .models import Price, Stuffs
from .forms import PriceForm


from datetime import datetime
from django.shortcuts import render, redirect
import jdatetime
from .forms import PriceForm
from .models import Price, Stuffs, Category

def add_price(request, date):
    try:
        price_instance = Price.objects.get(date=date)
        initial_data = {f'stuff_{stuff_id}': price for stuff_id, price in price_instance.prices.items()}
        print(initial_data)
    except:
        price_instance = None  # اختصاص دادن مقدار پیش‌فرض به price_instance
        initial_data = {}
        
    # Find the latest price record before the specified date
    if initial_data == {}:
        latest_price = Price.objects.filter(date__lt=date).order_by('-date').first()
        if latest_price:
            initial_data = {f'stuff_{stuff_id}': price for stuff_id, price in latest_price.prices.items()}
        else :
            initial_data = {f'stuff_{stuff.stuff_id}': '0' for stuff in Stuffs.objects.all()}
    
    if request.method == 'POST':
        form = PriceForm(request.POST, initial=initial_data)
        if form.is_valid():
            prices = form.cleaned_data['prices']
            if price_instance:
                price_instance.prices = prices
                price_instance.save()
            else:
                price_instance = Price.objects.create(date=date, prices=prices)

            # Get today's date
            today_date = datetime.now().strftime('%Y-%m-%d')
            return redirect(f'/foodstuff/price/{today_date}/')
    else:
        form = PriceForm(initial=initial_data)

    gregorian_date = datetime.strptime(date, '%Y-%m-%d')
    jalali_date = jdatetime.date.fromgregorian(date=gregorian_date).strftime('%Y/%m/%d')
    
    # Fetch all stuffs with related category and scale
    stuffs = Stuffs.objects.select_related('stuff_category').all()
    categories = Category.objects.all().order_by('cat_id')  # اضافه کردن دسته بندی‌ها

    return render(request, 'foodstuff/add_price.html', {
        'form': form,
        'jalali_date': jalali_date,
        'date': date,
        'stuffs': stuffs,
        'categories': categories,
    })
    
    
def delete_stuff(request, id):
    today_date = datetime.today().strftime('%Y-%m-%d')
    stuff = get_object_or_404(Stuffs, id=id)
    stuff.delete()
    return redirect(reverse('foodstuff:add_price', kwargs={'date': today_date}))
        