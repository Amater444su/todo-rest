# Generated by Django 3.1.6 on 2021-08-04 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0005_auto_20210803_2256'),
    ]

    operations = [
        migrations.AddField(
            model_name='groups',
            name='name',
            field=models.CharField(default='My group', max_length=50),
        ),
    ]
