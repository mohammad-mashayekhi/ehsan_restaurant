# Generated by Django 5.0.6 on 2024-05-30 15:36

import shortuuid.django_fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='foodStuffCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_id', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefgh12345', length=10, max_length=30, prefix='', unique=True)),
                ('cat_name', models.CharField(max_length=300)),
            ],
        ),
    ]
