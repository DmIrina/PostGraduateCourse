# Generated by Django 4.2.7 on 2023-11-25 19:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vstup', '0010_alter_entrant_tck'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrant',
            name='cathedra',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vstup.cathedra', verbose_name='Кафедра'),
        ),
        migrations.AddField(
            model_name='entrant',
            name='specialty',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vstup.specialty', verbose_name='Спеціальність'),
        ),
    ]
