# Generated by Django 3.1.4 on 2021-02-18 21:36

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('popup_messeges', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Messege',
            new_name='Message',
        ),
    ]
