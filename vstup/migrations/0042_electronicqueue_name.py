# Generated by Django 4.2.7 on 2023-12-16 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vstup', '0041_rename_datetime_electronicqueue_slot'),
    ]

    operations = [
        migrations.AddField(
            model_name='electronicqueue',
            name='name',
            field=models.CharField(default='-', max_length=50),
        ),
    ]
