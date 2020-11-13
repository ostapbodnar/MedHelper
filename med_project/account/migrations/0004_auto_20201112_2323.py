# Generated by Django 3.1.3 on 2020-11-12 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20201112_1605'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='baseuser',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='baseuser',
            name='is_admin',
        ),
        migrations.RemoveField(
            model_name='baseuser',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='baseuser',
            name='is_superuser',
        ),
        migrations.AddField(
            model_name='doctor',
            name='user_status',
            field=models.CharField(choices=[(1000, 'admin'), (0, 'patient'), (1, 'doctor')], default=1, max_length=20),
        ),
        migrations.AddField(
            model_name='patient',
            name='user_status',
            field=models.CharField(choices=[(1000, 'admin'), (0, 'patient'), (1, 'doctor')], default=0, max_length=20),
        ),
    ]
