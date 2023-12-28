# Generated by Django 4.2.7 on 2023-12-21 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vstup', '0048_alter_fundingsource_short_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fundingsource',
            old_name='short_name',
            new_name='shortName',
        ),
        migrations.AddField(
            model_name='educationform',
            name='shortName',
            field=models.CharField(default='Оч.Денна', max_length=10),
        ),
    ]