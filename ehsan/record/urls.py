
from django.urls import path, include
from .views import *

app_name='ehsan'

urlpatterns = [
    path('report/<str:date>/', report, name='report'),
]
