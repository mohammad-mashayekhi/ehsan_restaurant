# Generated by Django 4.2.13 on 2024-06-14 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0006_claimsdebts_claimsdebts_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='claimsdebts',
            name='type',
            field=models.CharField(choices=[('C', 'Claims'), ('D', 'Debts')], default=1, max_length=1),
            preserve_default=False,
        ),
    ]
