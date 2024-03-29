# Generated by Django 4.2.7 on 2023-12-21 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vstup', '0045_alter_entrant_electronic_queue'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrant',
            name='notes',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Примітки'),
        ),
        migrations.AlterField(
            model_name='entrant',
            name='approval_notification',
            field=models.BooleanField(default=False, verbose_name='Чи потребуєте повідомлення про допуск до вступних іспитів для оформлення за місцем роботи додаткової відпустки'),
        ),
        migrations.AlterField(
            model_name='entrant',
            name='dormitory_accommodation',
            field=models.BooleanField(default=False, verbose_name='Чи потребуєте поселення в гуртожиток на час складання вступних іспитів'),
        ),
    ]
