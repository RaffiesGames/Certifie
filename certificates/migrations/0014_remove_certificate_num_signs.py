# Generated by Django 3.0.7 on 2020-08-08 09:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('certificates', '0013_auto_20200808_1453'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certificate',
            name='num_signs',
        ),
    ]