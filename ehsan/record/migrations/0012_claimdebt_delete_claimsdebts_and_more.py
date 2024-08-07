# Generated by Django 4.2.13 on 2024-08-01 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0011_alter_monthlyreport_misc_expenses_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClaimDebt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(unique=True)),
                ('personal', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('company', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('specific_company', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('market', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('meat', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('other', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('staff', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('totalـclaims', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('totalـdebts', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('value_added_debt', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('level', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
            ],
            options={
                'verbose_name': 'ClaimDebt Report',
                'verbose_name_plural': 'ClaimDebt Reports',
                'ordering': ['-date'],
            },
        ),
        migrations.DeleteModel(
            name='ClaimsDebts',
        ),
        migrations.AlterModelOptions(
            name='monthlyreport',
            options={'ordering': ['-date'], 'verbose_name': 'Monthly Report', 'verbose_name_plural': 'Monthly Reports'},
        ),
    ]
