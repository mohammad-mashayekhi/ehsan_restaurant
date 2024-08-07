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
from django.conf.urls.static import static
from django.conf import settings 

app_name='ehsan'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('foodstuff/', include('foodstuff.urls')),
    path('repository/', include('repository.urls')),
    path('recipe/', include('recipe.urls')),
    path('record/', include('record.urls')),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    path('calendar', calendar, name='calendar'),
]


urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)  # media
urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT)  # static
