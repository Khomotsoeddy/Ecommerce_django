# Generated by Django 3.1.7 on 2023-03-12 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='age_number',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
