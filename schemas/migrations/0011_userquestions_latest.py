# Generated by Django 2.2 on 2020-05-12 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schemas', '0010_auto_20200510_2042'),
    ]

    operations = [
        migrations.AddField(
            model_name='userquestions',
            name='latest',
            field=models.TextField(blank=True),
        ),
    ]