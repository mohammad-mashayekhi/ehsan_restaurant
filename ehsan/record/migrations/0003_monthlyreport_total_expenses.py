# Generated by Django 4.2.13 on 2024-06-13 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0002_monthlyreport_total_sales'),
    ]

    operations = [
        migrations.AddField(
            model_name='monthlyreport',
            name='total_expenses',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
