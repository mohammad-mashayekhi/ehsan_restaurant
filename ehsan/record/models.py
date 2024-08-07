from django.db import models
from django.utils import timezone
from shortuuid.django_fields import ShortUUIDField

class MonthlyReport(models.Model):
    date = models.DateField(unique=True)
    sales_hall = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    sales_takeaway = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    sales_snappfood = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    sales_company = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    sales_special_company = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    sales_charity = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    sales_charity1 = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    sales_misc = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    total_sales = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    rent = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    salaries = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    hall = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    raw_materials = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    consumables = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    maintenance = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    delivery = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    misc_expenses = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    total_expenses = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    monthly_profit = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    profit_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    cost_to_sales_ratio = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    class Meta:
        ordering = ['-date']
        verbose_name = "Monthly Report"
        verbose_name_plural = "Monthly Reports"

    def __str__(self):
        return f"Report for {self.date}"

    def save(self, *args, **kwargs):
        # Ensure only month and year are stored in the date field
        if self.date:
            self.date = self.date.replace(day=1)
        super().save(*args, **kwargs)
        

class ClaimDebt(models.Model):
    personal = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    company = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    specific_company = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    
    market = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    meat = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    other = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    staff = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    
    total_claims = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    total_debts = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    value_added_debt = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    level = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    
    date = models.DateField()

    class Meta:
        ordering = ['-date']
        verbose_name = "ClaimDebt Report"
        verbose_name_plural = "ClaimDebt Reports"

    def __str__(self):
        return f"ClaimDebt Report for {self.date}"

    def save(self, *args, **kwargs):
        # Ensure only month and year are stored in the date field
        if self.date:
            self.date = self.date.replace(day=1)
        super().save(*args, **kwargs)