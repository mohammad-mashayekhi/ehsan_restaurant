# Generated by Django 5.0.6 on 2024-06-01 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodstuff', '0006_alter_price_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='price',
            name='prices',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]