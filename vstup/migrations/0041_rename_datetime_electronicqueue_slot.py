# Generated by Django 4.2.7 on 2023-12-15 19:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vstup', '0040_alter_electronicqueue_datetime'),
    ]

    operations = [
        migrations.RenameField(
            model_name='electronicqueue',
            old_name='datetime',
            new_name='slot',
        ),
    ]
