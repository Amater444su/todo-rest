# Generated by Django 3.1.6 on 2021-08-08 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0010_auto_20210805_0034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grouptask',
            name='status',
            field=models.CharField(choices=[('Not done', 'Not Done'), ('In process', 'In Process'), ('Done', 'Done'), ('Out of date', 'Out Of Date')], default='Not done', max_length=100),
        ),
    ]