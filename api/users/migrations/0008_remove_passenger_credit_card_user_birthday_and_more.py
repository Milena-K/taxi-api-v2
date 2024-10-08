# Generated by Django 5.1.1 on 2024-10-01 12:48

import phonenumber_field.modelfields
from django.db import (
    migrations,
    models,
)


class Migration(
    migrations.Migration
):
    dependencies = [
        (
            "users",
            "0007_remove_driver_rating",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="passenger",
            name="credit_card",
        ),
        migrations.AddField(
            model_name="user",
            name="birthday",
            field=models.DateField(
                auto_now=True
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="date_created",
            field=models.DateField(
                auto_now=True
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="phone_number",
            field=phonenumber_field.modelfields.PhoneNumberField(
                blank=True,
                max_length=128,
                region=None,
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                blank=True,
                max_length=254,
            ),
        ),
    ]
