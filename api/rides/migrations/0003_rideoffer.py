# Generated by Django 5.0.7 on 2024-08-01 11:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0002_alter_riderequest_passenger'),
        ('users', '0003_passenger_credit_card'),
    ]

    operations = [
        migrations.CreateModel(
            name='RideOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arrival_time', models.IntegerField()),
                ('price', models.FloatField()),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.driver')),
                ('ride', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rides.riderequest')),
            ],
        ),
    ]
