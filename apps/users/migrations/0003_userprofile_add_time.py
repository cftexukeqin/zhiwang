# Generated by Django 2.1.7 on 2020-05-28 14:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200528_2157'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='add_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]