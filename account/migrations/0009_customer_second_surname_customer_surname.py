# Generated by Django 4.1.7 on 2023-03-31 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0008_alter_address_phone_alter_customer_mobile"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="second_surname",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name="customer",
            name="surname",
            field=models.CharField(default="Masilela", max_length=150),
            preserve_default=False,
        ),
    ]