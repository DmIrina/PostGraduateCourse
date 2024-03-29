# Generated by Django 4.2.7 on 2023-12-11 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vstup', '0033_rename_cathedra_department_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entrant',
            name='filling_form_date',
        ),
        migrations.AddField(
            model_name='entrant',
            name='electronic_queue',
            field=models.CharField(max_length=16, null=True, verbose_name='Електронна черга'),
        ),
        migrations.AlterField(
            model_name='entrant',
            name='level',
            field=models.IntegerField(choices=[(1, 'Магістр (науковий рівень)'), (2, 'Магістр (професійний рівень)'), (3, 'Спеціаліст')], default=3, verbose_name='Рівень диплому про вищу освіту'),
        ),
    ]
