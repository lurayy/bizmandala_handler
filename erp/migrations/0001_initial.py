# Generated by Django 3.0.3 on 2020-11-06 06:19

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('commerce', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PortMan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server_name', models.CharField(default='0.0.0.0', max_length=255)),
                ('current_port', models.PositiveIntegerField(default='9000')),
                ('available_ports', models.TextField(default='[]')),
            ],
        ),
        migrations.CreateModel(
            name='ERP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('company', models.CharField(max_length=255)),
                ('address', models.TextField(max_length=255)),
                ('container_id', models.TextField(blank=True, null=True)),
                ('db_container_id', models.TextField(blank=True, null=True)),
                ('network_id', models.TextField(blank=True, null=True)),
                ('link', models.TextField(blank=True, null=True)),
                ('ip', models.CharField(blank=True, max_length=20)),
                ('port', models.PositiveIntegerField(blank=True, default=9000, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('credit', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='erp', to='commerce.Credit')),
            ],
        ),
    ]
