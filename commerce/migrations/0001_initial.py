# Generated by Django 3.0.3 on 2020-11-04 07:22

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Credit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('left_days', models.PositiveIntegerField()),
                ('used_days', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('bill_amount', models.FloatField()),
                ('paid_amount', models.FloatField()),
                ('pure_total_amount', models.FloatField()),
                ('discount_amount', models.FloatField(default=0)),
                ('discount_note', models.TextField()),
                ('payment_verification', models.TextField()),
                ('time_in_days', models.PositiveIntegerField()),
                ('number_of_erps', models.PositiveIntegerField()),
                ('is_refunded', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_paid', models.BooleanField(default=False)),
                ('is_converted_to_credits', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unitary_price', models.FloatField()),
            ],
        ),
    ]
