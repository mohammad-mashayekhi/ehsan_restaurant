from django.contrib import admin
from django.urls import path, include
from .views import *


app_name='accounting'

urlpatterns = [
    path('report/<int:year>/<int:month>/', month_report_view, name='month_report_view'),
]
