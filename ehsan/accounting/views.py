
from django.utils import timezone
from .models import DailyReport
from .forms import DailyReportForm
from django.shortcuts import render, redirect
from datetime import datetime

def month_report_view(request, year, month):
    # تبدیل سال و ماه به اعداد صحیح
    year = int(year)
    month = int(month)
    
    # تنظیم تاریخ به اولین روز از ماه
    report_date = datetime(year=year, month=month, day=1)
    
    # بارگذاری گزارش ماهانه اگر وجود داشته باشد
    try:
        report = DailyReport.objects.get(date__year=year, date__month=month)
        created = False
    except DailyReport.DoesNotExist:
        report = None
        created = True
    
    if request.method == 'POST':
        form = DailyReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect('accounting:month_report_view', year=year, month=month)
    else:
        form = DailyReportForm(instance=report)

    context = {
        'form': form,
        'date': report_date.strftime('%Y-%m'),  # تبدیل تاریخ به فرمت ماه و سال
    }
    return render(request, 'accounting/month_report_form.html', context)