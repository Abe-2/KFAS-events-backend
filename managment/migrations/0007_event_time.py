# Generated by Django 3.0.2 on 2020-02-05 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managment', '0006_auto_20200205_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='time',
            field=models.TimeField(null=True),
        ),
    ]