# Generated by Django 4.2.15 on 2024-10-16 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_listing_id_alter_listingcategory_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listingcategory',
            name='title',
            field=models.CharField(max_length=228, unique=True),
        ),
    ]