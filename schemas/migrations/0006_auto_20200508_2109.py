# Generated by Django 2.2 on 2020-05-08 21:09

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schemas', '0005_auto_20200508_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schema',
            name='questions',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True), size=10), size=None),
        ),
    ]
