# Generated by Django 3.1.2 on 2020-12-21 05:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_handler', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userbase',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterUniqueTogether(
            name='userbase',
            unique_together=set(),
        ),
    ]
