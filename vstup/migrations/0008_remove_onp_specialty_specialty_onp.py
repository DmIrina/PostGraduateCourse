# Generated by Django 4.2.7 on 2023-11-25 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vstup', '0007_remove_onp_cathedra_cathedra_specialty_onp_specialty'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='onp',
            name='specialty',
        ),
        migrations.AddField(
            model_name='specialty',
            name='onp',
            field=models.ManyToManyField(help_text='ОНП', to='vstup.onp'),
        ),
    ]
