# Generated by Django 5.1.1 on 2025-01-27 18:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("rides", "0001_initial"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="ride",
            name="driver",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="users.driver"
            ),
        ),
        migrations.AddField(
            model_name="ride",
            name="passenger",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="users.passenger"
            ),
        ),
        migrations.AddField(
            model_name="rating",
            name="ride",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="rides.ride"
            ),
        ),
    ]
