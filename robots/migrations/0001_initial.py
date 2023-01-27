# Generated by Django 4.1.1 on 2022-11-11 08:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wagtailcore", "0076_modellogentry_revision"),
    ]

    operations = [
        migrations.CreateModel(
            name="Robots",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("contents", models.TextField(blank=True)),
                (
                    "site",
                    models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to="wagtailcore.site"),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]