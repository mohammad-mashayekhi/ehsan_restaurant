from datetime import datetime
from django.shortcuts import render, redirect
from .models import MonthlyReport
from .forms import DailyReportForm

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
