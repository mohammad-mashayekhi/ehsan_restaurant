"""
URL configuration for ehsan project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import *

app_name='foodstuff'

urlpatterns = [
    # path('', foodstuffs , name='foodstuffs'),
    path('add', addfoodstuffs , name='addfoodstuffs'),
    path('edit-stuff/<str:id>/', edit_stuff, name='edit_stuff'),
    
    path('price/<str:date>/', add_price, name='add_price'),
    path('delete/<int:id>/', delete_stuff, name='delete_stuff'),

]
