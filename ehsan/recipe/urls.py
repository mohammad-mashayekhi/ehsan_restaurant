
from django.urls import path, include
from .views import *

app_name='recipe'

urlpatterns = [
    path('add/', add_recipe, name='add_recipe'),
    path('edit/<int:id>', edit_recipe, name='edit_recipe'),
    path('', recipe_list, name='recipe_list'),
    path('save_recipe_prices_ajax/', save_recipe_prices_ajax, name='save_recipe_prices_ajax'),
    path('calculator', recipe_calculator, name='recipe_calculator'),

]
