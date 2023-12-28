# Generated by Django 4.2.7 on 2023-12-25 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vstup', '0050_alter_entrant_diploma_avg_alter_entrant_diploma_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrant',
            name='approval_notification',
            field=models.BooleanField(default=False, verbose_name='Повідомити про допуск до іспитів для оформлення відпустки'),
        ),
        migrations.AlterField(
            model_name='entrant',
            name='diploma_avg',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=5, verbose_name='Середній бал'),
        ),
        migrations.AlterField(
            model_name='entrant',
            name='dormitory_accommodation',
            field=models.BooleanField(default=False, verbose_name='Потреба поселення в гуртожиток на час іспитів'),
        ),
        migrations.AlterField(
            model_name='entrant',
            name='grade_scientific_achievements',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6, null=True, verbose_name='Наукові досягнення'),
        ),
    ]