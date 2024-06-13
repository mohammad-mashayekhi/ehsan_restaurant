from django.db import models

from django.db import models

class DailyReport(models.Model):
    date = models.DateField(unique=True)
    sales_hall = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    sales_takeaway = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    sales_snappfood = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    sales = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    sales_company = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    sales_special_company = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    sales_charity = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    sales_misc = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    
    rent = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    salaries = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    overtime = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    raw_materials = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    consumables = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    maintenance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    staff_meals = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    misc_expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    
    monthly_profit = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    profit_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    cost_to_sales_ratio = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    class Meta:
        ordering = ['-date']
        verbose_name = "Daily Report"
        verbose_name_plural = "Daily Reports"

    def __str__(self):
        return f"Report for {self.date}"

    @property
    def total_sales(self):
        return (self.sales_hall + self.sales_takeaway + self.sales_snapfood +
                self.sales_orders + self.sales_company + self.sales_special_company +
                self.sales_charity + self.sales_misc)

    @property
    def total_expenses(self):
        return (self.rent + self.salaries + self.overtime + self.raw_materials +
                self.consumables + self.current_expenses + self.staff_meals +
                self.expenses_misc)
