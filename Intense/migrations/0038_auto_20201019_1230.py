# Generated by Django 2.2.15 on 2020-10-19 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Intense', '0037_banner_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='is_active',
            field=models.BooleanField(blank=True, default=True),
        ),
    ]