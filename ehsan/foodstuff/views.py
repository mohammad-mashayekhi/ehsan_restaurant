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

def edit_stuff(request, pk):
    today_date = datetime.today().strftime('%Y-%m-%d')
    stuff = get_object_or_404(Stuffs, pk=pk)
    if request.method == "POST":
        form = StuffsForm(request.POST, instance=stuff)
        if form.is_valid():
            form.save()
            return redirect(reverse('foodstuff:add_price', kwargs={'date': today_date}))
    else:
        form = StuffsForm(instance=stuff)
    return render(request, 'foodstuff/edit_stuff.html', {'form': form})


from django.shortcuts import render, redirect
from .models import Price, Stuffs
from .forms import PriceForm
import jdatetime
from datetime import datetime

def add_price(request, date):
    price_instance = None
    try:
        price_instance = Price.objects.get(date=date)
        initial_data = {'prices': price_instance.prices}
    except Price.DoesNotExist:
        initial_data = None

    if price_instance:
        initial_data = {'stuff_' + str(stuff_id): price for stuff_id, price in price_instance.prices.items()}

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
    categories = Category.objects.all()  # اضافه کردن دسته بندی‌ها

    return render(request, 'foodstuff/add_price.html', {
        'form': form,
        'jalali_date': jalali_date,
        'date':date,
        'stuffs': stuffs,
        'categories':categories,
    })