# Generated by Django 2.2 on 2020-05-08 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schemas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schema',
            name='image',
            field=models.ImageField(upload_to='.images/'),
        ),
    ]