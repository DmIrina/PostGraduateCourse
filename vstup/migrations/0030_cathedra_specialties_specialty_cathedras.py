# Generated by Django 4.2.7 on 2023-12-03 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vstup', '0029_entrant_additional_tests_entrant_competition_score_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cathedra',
            name='specialties',
            field=models.ManyToManyField(help_text='Спеціальність', to='vstup.specialty'),
        ),
        migrations.AddField(
            model_name='specialty',
            name='cathedras',
            field=models.ManyToManyField(help_text='Кафедра', to='vstup.cathedra'),
        ),
    ]