# Generated by Django 5.0.7 on 2024-07-25 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.CharField(blank=True),
        ),
    ]
