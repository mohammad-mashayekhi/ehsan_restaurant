from django.db import models
from django.utils import timezone
from shortuuid.django_fields import ShortUUIDField

class MonthlyReport(models.Model):
    date = models.DateField(unique=True)
    sales_hall = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    sales_takeaway = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    sales_snappfood = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    sales_company = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    sales_special_company = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    sales_charity = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    sales_charity1 = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    sales_misc = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    rent = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    salaries = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    hall = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    raw_materials = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    consumables = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    maintenance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    delivery = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    misc_expenses = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    total_expenses = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    monthly_profit = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    profit_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    cost_to_sales_ratio = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    class Meta:
        ordering = ['-date']
        verbose_name = "Daily Report"
        verbose_name_plural = "Daily Reports"

    def __str__(self):
        return f"Report for {self.date}"

    def save(self, *args, **kwargs):
        # Ensure only month and year are stored in the date field
        if self.date:
            self.date = self.date.replace(day=1)
        super().save(*args, **kwargs)
        

class ClaimsDebts(models.Model):
    CLAIM = 'claim'
    DEBT = 'debt'
    
    TYPE_CHOICES = [
        (CLAIM, 'طلب'),
        (DEBT, 'بدهی'),
    ]
    
    claimsdebts_id = ShortUUIDField(editable=True, unique=True, length=10, max_length=30, alphabet="abcdefgh12345")
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    ingredients = models.JSONField(default=dict, null=True, blank=True)
    date_created = models.DateField(default=timezone.now)

    def __str__(self):
        return f"({self.get_type_display()}) {self.date_created}"
