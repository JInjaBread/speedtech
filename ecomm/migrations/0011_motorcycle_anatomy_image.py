# Generated by Django 4.0.5 on 2022-08-30 22:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ecomm', '0010_remove_product_old_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='motorcycle',
            name='anatomy_image',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='motorcycle_anatomy'),
            preserve_default=False,
        ),
    ]
