# Generated by Django 5.1.5 on 2025-01-25 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='city_name',
            field=models.CharField(max_length=40, unique=True),
        ),
    ]
