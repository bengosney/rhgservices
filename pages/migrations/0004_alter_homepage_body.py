# Generated by Django 4.0.2 on 2022-03-20 19:44

from django.db import migrations
import pages.blocks
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_alter_homepage_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='body',
            field=wagtail.fields.StreamField([('Callout', pages.blocks.CallOutBlock()), ('InfoPod', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('title', wagtail.blocks.CharBlock()), ('paragraph', wagtail.blocks.CharBlock(help_text='Optional', required=False))]))), ('InfoPods', wagtail.blocks.StreamBlock([('infopod', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('title', wagtail.blocks.CharBlock()), ('paragraph', wagtail.blocks.CharBlock(help_text='Optional', required=False))]))])), ('paragraph', wagtail.blocks.RichTextBlock())]),
        ),
    ]
