# Generated by Django 3.1.6 on 2021-08-08 10:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0011_auto_20210808_1346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groups',
            name='task_amount',
        ),
    ]
