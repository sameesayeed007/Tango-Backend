# Generated by Django 2.2.15 on 2020-10-01 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Intense', '0006_auto_20201001_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cupons',
            name='start_from',
            field=models.DateField(blank=True, null=True),
        ),
    ]