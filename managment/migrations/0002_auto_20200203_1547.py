# Generated by Django 3.0.2 on 2020-02-03 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('managment', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='creator',
            new_name='created_by',
        ),
    ]