# Generated by Django 4.0.4 on 2022-05-16 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0018_remove_sitesettings_google_maps_api_key_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesettings',
            name='checkatrade',
            field=models.URLField(default='', help_text='Your checkatrade link', max_length=255),
        ),
    ]
