
from django.urls import path, include
from .views import *

app_name='recipe'

urlpatterns = [
    path('add/', add_recipe, name='add_recipe'),
    path('edit/<int:recipe_id>', edit_recipe, name='edit_recipe'),
    path('', recipe_list, name='recipe_list'),
]
