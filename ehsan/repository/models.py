from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.contrib.postgres.fields import JSONField
from django.utils import timezone


class Repository(models.Model):
    ENTRY_TYPES = (
        ('in', 'ورودی'),
        ('out', 'خروجی'),
    )

    id = ShortUUIDField(primary_key=True)
    date = models.DateField(default=timezone.now)
    type = models.CharField(max_length=3, choices=ENTRY_TYPES, default='in')
    quantities = models.JSONField(default=dict, null=True, blank=True)

    def __str__(self):
        return f"انبار روز {self.date} - {'ورودی' if self.type == 'in' else 'خروجی'}"