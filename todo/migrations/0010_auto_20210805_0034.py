# Generated by Django 3.1.6 on 2021-08-04 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0009_auto_20210805_0032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grouptask',
            name='status',
            field=models.CharField(choices=[('not_done', 'Not done'), ('in_process', 'In process'), ('done', 'Done'), ('out_of_date', 'Out of date')], default='Not done', max_length=100),
        ),
    ]
