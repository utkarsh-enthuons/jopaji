# Generated by Django 5.0.2 on 2024-02-11 19:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jopaji', '0003_remove_tbl_product_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tbl_product',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='tbl_product',
            name='gst',
        ),
        migrations.RemoveField(
            model_name='tbl_product',
            name='images',
        ),
        migrations.RemoveField(
            model_name='tbl_product',
            name='price_in_gst',
        ),
        migrations.RemoveField(
            model_name='tbl_product',
            name='sell_price',
        ),
        migrations.AddField(
            model_name='tbl_product',
            name='flavour',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='tbl_product',
            name='image1',
            field=models.ImageField(default=True, upload_to='images/product/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])]),
        ),
        migrations.AddField(
            model_name='tbl_product',
            name='image2',
            field=models.ImageField(blank=True, upload_to='images/product/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])]),
        ),
        migrations.AddField(
            model_name='tbl_product',
            name='image3',
            field=models.ImageField(blank=True, upload_to='images/product/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])]),
        ),
        migrations.AddField(
            model_name='tbl_product',
            name='image4',
            field=models.ImageField(blank=True, upload_to='images/product/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])]),
        ),
        migrations.AddField(
            model_name='tbl_product',
            name='image5',
            field=models.ImageField(blank=True, upload_to='images/product/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])]),
        ),
    ]
