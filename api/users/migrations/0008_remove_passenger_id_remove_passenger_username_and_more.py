# Generated by Django 5.0.7 on 2024-07-28 13:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_passenger'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='passenger',
            name='id',
        ),
        migrations.RemoveField(
            model_name='passenger',
            name='username',
        ),
        migrations.AddField(
            model_name='passenger',
            name='credit_card',
            field=models.CharField(blank=True),
        ),
        migrations.AddField(
            model_name='passenger',
            name='user_ptr',
            field=models.OneToOneField(auto_created=True, default=1, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
    ]
