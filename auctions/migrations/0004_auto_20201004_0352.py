# Generated by Django 3.1.1 on 2020-10-04 03:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20201003_0533'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Listings',
            new_name='Listing',
        ),
    ]
