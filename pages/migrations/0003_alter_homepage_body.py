# Generated by Django 4.0.2 on 2022-03-20 19:37

from django.db import migrations
import pages.blocks
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_alter_homepage_body_alter_infopage_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='body',
            field=wagtail.core.fields.StreamField([('Callout', pages.blocks.CallOutBlock()), ('InfoPod', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('title', wagtail.core.blocks.CharBlock()), ('paragraph', wagtail.core.blocks.CharBlock(help_text='Optional', required=False))])), ('InfoPods', wagtail.core.blocks.StreamBlock([('infopod', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('title', wagtail.core.blocks.CharBlock()), ('paragraph', wagtail.core.blocks.CharBlock(help_text='Optional', required=False))]))])), ('paragraph', wagtail.core.blocks.RichTextBlock())]),
        ),
    ]
