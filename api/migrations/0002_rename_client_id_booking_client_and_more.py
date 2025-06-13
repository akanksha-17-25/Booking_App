# Generated by Django 4.2.22 on 2025-06-05 00:06

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="booking",
            old_name="client_id",
            new_name="client",
        ),
        migrations.RenameField(
            model_name="booking",
            old_name="slot_id",
            new_name="slot",
        ),
        migrations.AlterUniqueTogether(
            name="booking",
            unique_together={("client", "slot")},
        ),
    ]
