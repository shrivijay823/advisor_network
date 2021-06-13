# Generated by Django 3.2.1 on 2021-05-21 05:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('advisor_network_app', '0014_auto_20210521_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='u_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
