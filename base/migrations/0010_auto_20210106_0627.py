# Generated by Django 3.1.4 on 2021-01-06 00:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_kitchen_cover_radius'),
    ]

    operations = [
        migrations.RenameField(
            model_name='kitchen',
            old_name='cover_radius',
            new_name='cover_radius_in_kms',
        ),
    ]
