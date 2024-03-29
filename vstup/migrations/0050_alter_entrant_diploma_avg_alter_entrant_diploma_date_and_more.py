# Generated by Django 4.2.7 on 2023-12-25 01:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vstup', '0049_rename_short_name_fundingsource_shortname_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrant',
            name='diploma_avg',
            field=models.DecimalField(decimal_places=1, default=0.0, help_text='Середній бал диплому про вищу освіту (зазначений у додатку до диплому)', max_digits=5, verbose_name='Середній бал'),
        ),
        migrations.AlterField(
            model_name='entrant',
            name='diploma_date',
            field=models.DateField(default='1980-01-01', verbose_name='Дата в/диплому'),
        ),
        migrations.AlterField(
            model_name='entrant',
            name='diploma_specialty',
            field=models.CharField(default='000', max_length=50, verbose_name='Спеціальність (в дипломі)'),
        ),
        migrations.AlterField(
            model_name='entrant',
            name='foreign_language',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vstup.foreignlanguage', verbose_name='Іноземна мова'),
        ),
        migrations.AlterField(
            model_name='entrant',
            name='funding_source',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vstup.fundingsource', verbose_name='Фінансування'),
        ),
        migrations.AlterField(
            model_name='entrant',
            name='phone',
            field=models.CharField(max_length=20, verbose_name='Телефон '),
        ),
        migrations.AlterField(
            model_name='entrant',
            name='scientific_advisor',
            field=models.CharField(max_length=20, verbose_name='Керівник'),
        ),
        migrations.AlterField(
            model_name='entrant',
            name='specialty',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vstup.specialty', verbose_name='Спеціальність'),
        ),
        migrations.AlterField(
            model_name='university',
            name='educationTypeName',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='university',
            name='financingTypeName',
            field=models.CharField(max_length=50),
        ),
    ]
