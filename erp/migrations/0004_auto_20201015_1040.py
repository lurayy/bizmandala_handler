# Generated by Django 3.1.2 on 2020-10-15 10:40

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0003_erp_ip'),
    ]

    operations = [
        migrations.AddField(
            model_name='erp',
            name='db_container_id',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='erp',
            name='network_id',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='erp',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]