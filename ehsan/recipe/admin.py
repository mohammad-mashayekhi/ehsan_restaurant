from django.contrib import admin
from .models import *

admin.site.register(Recipe)
admin.site.register(RecipePrice)
admin.site.register(RecipeSaleFile)

