# Generated by Django 4.0.5 on 2022-11-03 06:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecomm', '0013_alter_motorcycle_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomm.category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='motorcycle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomm.motorcycle'),
        ),
    ]
