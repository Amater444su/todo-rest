# Generated by Django 3.1.6 on 2021-08-10 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0012_remove_groups_task_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='grouptask',
            name='id_group',
            field=models.PositiveIntegerField(default=0),
        ),
    ]