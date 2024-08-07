from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils import timezone

class Recipe(models.Model):
    recipe_id = ShortUUIDField(editable=True,unique=True, length=10, max_length=30, alphabet="abcdefgh12345")
    name = models.CharField(max_length=300)
    ingredients = models.JSONField(default=dict, null=True, blank=True)
    date_created = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name

class RecipePrice(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    recipe_prices = models.JSONField()

    def __str__(self):
        return str(self.created_at)
    
    
class RecipeSaleFile(models.Model):
    created_at = models.DateField(auto_now_add=True)
    date_created = models.DateField(default=timezone.now)
    recipe_prices = models.JSONField()

    def __str__(self):
        return str(self.date_created)    