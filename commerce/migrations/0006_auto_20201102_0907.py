# Generated by Django 3.1.2 on 2020-11-02 09:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0005_auto_20201102_0757'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Bundle',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='is_bundle',
        ),
    ]