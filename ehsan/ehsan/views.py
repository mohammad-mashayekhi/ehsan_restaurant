from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
# from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
import jdatetime
from datetime import datetime

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.POST.get('next', 'dashboard')  # پیش‌فرض 'dashboard'
                return redirect(next_url)  # به صفحه اصلی یا صفحه دلخواه خودتان ریدایرکت کنید
            else:
                form.add_error(None, 'نام کاربری یا رمز عبور اشتباه است.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'main/login.html', {'form': form, 'next': request.GET.get('next', '')})

def logout_view(request):
    logout(request)
    return redirect('dashboard')  # به صفحه اصلی یا هر صفحه دیگری که می‌خواهید کاربر بعد از خروج به آن هدایت شود.

from django.shortcuts import render
from repository.models import Repository
from foodstuff.models import Price
from recipe.models import RecipeSaleFile
from record.models import ClaimDebt,MonthlyReport



@login_required
def dashboard(request):
    import jdatetime
    from datetime import datetime,timedelta
    from django.utils import timezone

    today_date = datetime.now().strftime('%Y-%m-%d')
    gregorian_date = datetime.strptime(today_date, '%Y-%m-%d')
    jalali_date = jdatetime.date.fromgregorian(date=gregorian_date).strftime('%Y/%m/%d')
    
    def convert_to_jalali(gregorian_date):
        if gregorian_date:
            return jdatetime.date.fromgregorian(date=gregorian_date).strftime('%Y/%m/%d')
        return None
    
    def is_today(gregorian_date):
        if gregorian_date:
            return gregorian_date == datetime.now().date()
        return False

    def is_within_last_month(gregorian_date):
            if gregorian_date:
                now = timezone.now().date()
                one_month_ago = now - timedelta(days=30)
                return gregorian_date >= one_month_ago
            return False
        
    def is_within_last_two_weeks(date):
        if gregorian_date:
            now = timezone.now().date()
            two_weeks_ago = now - timedelta(days=14)
            return date >= two_weeks_ago    
        return False

    # دریافت آخرین ورودی انبار
    last_entry_in = Repository.objects.filter(type='in').order_by('-date').first()
    last_entry_in_today = is_today(last_entry_in.date) if last_entry_in else False

    # دریافت آخرین خروجی انبار
    last_entry_out = Repository.objects.filter(type='out').order_by('-date').first()
    last_entry_out_today = is_today(last_entry_out.date) if last_entry_out else False

    # دریافت آخرین اطلاعات فروش
    last_sale_info = RecipeSaleFile.objects.order_by('-date_created').first()
    last_sale_info_today = is_today(last_sale_info.date_created) if last_sale_info else False

    # دریافت آخرین زمان آپدیت قیمت مواد اولیه
    last_price_update = Price.objects.order_by('-date').first()
    last_price_update_recent = is_within_last_month(last_price_update.date) if last_price_update else False

    # بررسی اینکه آیا رکوردی در دو هفته اخیر در ClaimsDebts ایجاد شده است یا خیر
    two_weeks_ago = timezone.now() - timedelta(days=14)
    recent_claims_debts = ClaimsDebts.objects.filter(date_created__gte=two_weeks_ago).exists()

    # دریافت آخرین زمان آپدیت گزارشات حسابداری
    last_MonthlyReport_update = MonthlyReport.objects.order_by('-date').first()
    last_MonthlyReport_update_recent = is_within_last_month(last_MonthlyReport_update.date) if last_MonthlyReport_update else False


    context = {
        'today_date':today_date,
        'jalali_date': jalali_date,
        'last_entry_in_today': last_entry_in_today,
        'last_entry_out_today': last_entry_out_today,
        'last_sale_info_today': last_sale_info_today,
        'last_price_update_recent': last_price_update_recent,
        'last_MonthlyReport_update_recent': last_MonthlyReport_update_recent,
        'recent_claims_debts': recent_claims_debts,
    }
    return render(request, 'main/dashboard.html', context)

def calendar(request):
    pass
    return render(request, 'main/calendar.html')
    