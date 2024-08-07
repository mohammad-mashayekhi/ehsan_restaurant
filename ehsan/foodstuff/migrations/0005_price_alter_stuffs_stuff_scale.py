# Generated by Django 5.0.6 on 2024-06-01 03:10

import shortuuid.django_fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodstuff', '0004_remove_stuffs_stuff_category_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_id', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefgh12345', length=10, max_length=30, prefix='', unique=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('prices', models.JSONField(blank=True, default=list)),
            ],
        ),
        migrations.AlterField(
            model_name='stuffs',
            name='stuff_scale',
            field=models.CharField(choices=[('Weight', 'وزن (کیلوگرم)'), ('Number', 'عدد (تعداد)')], default='Weight', max_length=20),
        ),
    ]
