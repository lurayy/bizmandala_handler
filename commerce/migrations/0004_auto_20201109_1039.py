# Generated by Django 3.1.2 on 2020-11-09 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0003_auto_20201109_0850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credit',
            name='left_days',
            field=models.IntegerField(),
        ),
    ]
