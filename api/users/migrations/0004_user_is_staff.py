# Generated by Django 5.0.7 on 2024-08-06 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_passenger_credit_card'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]