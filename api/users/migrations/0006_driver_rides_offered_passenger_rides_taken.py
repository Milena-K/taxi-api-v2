# Generated by Django 5.0.7 on 2024-08-29 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_groups_user_is_active_user_is_superuser_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='rides_offered',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='passenger',
            name='rides_taken',
            field=models.IntegerField(default=0),
        ),
    ]
