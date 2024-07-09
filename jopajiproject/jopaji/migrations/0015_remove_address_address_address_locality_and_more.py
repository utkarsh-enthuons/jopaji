# Generated by Django 5.0.2 on 2024-02-26 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jopaji', '0014_cart_orderplaced'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='address',
        ),
        migrations.AddField(
            model_name='address',
            name='locality',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='address',
            name='state',
            field=models.CharField(choices=[('default', 'Select State'), ('andaman_and_nicobar_islands', 'Andaman and Nicobar Islands'), ('andhra_pradesh', 'Andhra Pradesh'), ('arunachal_pradesh', 'Arunachal Pradesh'), ('assam', 'Assam'), ('bihar', 'Bihar'), ('chandigarh', 'Chandigarh'), ('chhattisgarh', 'Chhattisgarh'), ('dadra_and_nagar_haveli', 'Dadra and Nagar Haveli'), ('daman_and_diu', 'Daman and Diu'), ('delhi', 'Delhi'), ('goa', 'Goa'), ('gujarat', 'Gujarat'), ('haryana', 'Haryana'), ('himachal_pradesh', 'Himachal Pradesh'), ('jammu_and_kashmir', 'Jammu and Kashmir'), ('jharkhand', 'Jharkhand'), ('karnataka', 'Karnataka'), ('kerala', 'Kerala'), ('ladakh', 'Ladakh'), ('lakshadweep', 'Lakshadweep'), ('madhya_pradesh', 'Madhya Pradesh'), ('maharashtra', 'Maharashtra'), ('manipur', 'Manipur'), ('meghalaya', 'Meghalaya'), ('mizoram', 'Mizoram'), ('nagaland', 'Nagaland'), ('odisha', 'Odisha'), ('puducherry', 'Puducherry'), ('punjab', 'Punjab'), ('rajasthan', 'Rajasthan'), ('sikkim', 'Sikkim'), ('tamil_nadu', 'Tamil Nadu'), ('telangana', 'Telangana'), ('tripura', 'Tripura'), ('uttar_pradesh', 'Uttar Pradesh'), ('uttarakhand', 'Uttarakhand'), ('west_bengal', 'West Bengal')], default='default', max_length=50),
        ),
    ]