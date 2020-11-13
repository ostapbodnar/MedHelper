# Generated by Django 3.1.3 on 2020-11-12 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20201112_2323'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseuser',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='baseuser',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='baseuser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='baseuser',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
