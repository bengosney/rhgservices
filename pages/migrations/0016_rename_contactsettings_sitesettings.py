# Generated by Django 4.0.2 on 2022-04-05 19:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0066_collection_management_permissions'),
        ('pages', '0015_alter_contactsettings_phone_number'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ContactSettings',
            new_name='SiteSettings',
        ),
    ]
