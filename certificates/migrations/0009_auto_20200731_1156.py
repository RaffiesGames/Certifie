# Generated by Django 3.0.8 on 2020-07-31 06:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certificates', '0008_auto_20200731_1155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='font_size1',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(72)]),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='font_size2',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(72)]),
        ),
    ]
