# Generated by Django 5.0.7 on 2024-09-18 13:20

import django.db.models.deletion
import django.utils.timezone
from django.db import (
    migrations,
    models,
)


class Migration(
    migrations.Migration
):
    dependencies = [
        (
            "rides",
            "0005_remove_rideoffer_driver_and_more",
        ),
        (
            "users",
            "0007_remove_driver_rating",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="ride",
            name="dropoff_time",
            field=models.DateTimeField(
                default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="ride",
            name="ride_duration",
            field=models.IntegerField(
                default=0
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="ride",
            name="ride_uuid",
            field=models.UUIDField(
                default=0,
                unique=True,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="ride",
            name="status",
            field=models.IntegerField(
                choices=[
                    (
                        0,
                        "Created",
                    ),
                    (
                        1,
                        "Active",
                    ),
                    (
                        2,
                        "Completed",
                    ),
                    (
                        3,
                        "Canceled",
                    ),
                ],
                default=0,
            ),
        ),
        migrations.AlterField(
            model_name="ride",
            name="end_time",
            field=models.DateTimeField(
                blank=True
            ),
        ),
        migrations.AlterField(
            model_name="ride",
            name="start_time",
            field=models.DateTimeField(
                blank=True
            ),
        ),
        migrations.CreateModel(
            name="Rating",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "rating",
                    models.FloatField(
                        default=5.0
                    ),
                ),
                (
                    "comment",
                    models.CharField(),
                ),
                (
                    "driver",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.driver",
                    ),
                ),
                (
                    "passenger",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.passenger",
                    ),
                ),
                (
                    "ride",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="rides.ride",
                    ),
                ),
            ],
        ),
    ]
