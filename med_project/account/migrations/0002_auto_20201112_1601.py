# Generated by Django 3.1.3 on 2020-11-12 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='baseuser',
            options={},
        ),
        migrations.AlterModelOptions(
            name='doctor',
            options={},
        ),
        migrations.AlterModelOptions(
            name='patient',
            options={},
        ),
        migrations.RemoveField(
            model_name='baseuser',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='baseuser',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='baseuser',
            name='user_permissions',
        ),
    ]
