# Generated by Django 4.2.7 on 2023-12-01 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vstup', '0025_entrant_approval_notification_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrant',
            name='scientific_advisor',
            field=models.CharField(max_length=20, verbose_name='Прізвище передбачуваного наукового керівника'),
        ),
    ]
