# Generated by Django 3.1.3 on 2020-12-07 21:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assignment', '0002_auto_20201207_2113'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='creator_id',
        ),
        migrations.AddField(
            model_name='assignment',
            name='creator',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='creator', to='account.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='assignment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]