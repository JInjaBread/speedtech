# Generated by Django 4.0.5 on 2022-07-18 06:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecomm', '0009_alter_motorcycle_company'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='old_price',
        ),
    ]