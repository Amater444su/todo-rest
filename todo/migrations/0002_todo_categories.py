# Generated by Django 3.1.6 on 2021-07-30 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='categories',
            field=models.CharField(blank=True, choices=[('Домашнее задание', 'Homework'), ('Дела по дому', 'Housework')], max_length=40, null=True),
        ),
    ]
