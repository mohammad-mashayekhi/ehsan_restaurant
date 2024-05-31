from django.db import models
from shortuuid.django_fields import ShortUUIDField


SCALE = [
    ("Weight", "وزن (کیلوگرم)"),
    ("Number", "عدد (تعداد)"),
] 

class Category(models.Model):
    cat_id = ShortUUIDField(unique=True , length=10 , max_length=30 , alphabet="abcdefgh12345")
    cat_name = models.CharField(max_length = 300)

    def __str__(self):
         return self.cat_name


class Stuffs(models.Model):
    stuff_id = ShortUUIDField(unique=True , length=10 , max_length=30 , alphabet="abcdefgh12345")
    stuff_name = models.CharField(max_length = 300)
    stuff_category = models.ForeignKey(Category, related_name='stuffs', on_delete=models.CASCADE)
    stuff_scale = models.CharField(choices=SCALE , max_length=20 , default="Weight")

    def __str__(self):
         return self.stuff_name
