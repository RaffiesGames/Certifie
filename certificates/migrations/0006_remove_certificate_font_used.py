# Generated by Django 3.0.8 on 2020-07-30 08:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('certificates', '0005_certificate_font_used'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certificate',
            name='font_used',
        ),
    ]
