# Generated by Django 5.0.2 on 2024-02-11 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jopaji', '0002_tbl_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tbl_product',
            name='image',
        ),
    ]