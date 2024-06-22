
from django.urls import path, include
from .views import *

app_name='record'

urlpatterns = [
    path('report/<str:date>/', report, name='report'),
    path('claimsdebts/<str:date>/', add_claimsdebts, name='claimsdebts'),
    path('consumptionreport/<str:date>/', consumptionreport, name='consumptionreport'),
    path('chart/<str:date>/', reportchart, name='reportchart'),
]
