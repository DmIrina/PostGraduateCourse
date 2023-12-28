from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User
from phonenumbers import parse, is_valid_number
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
# from .managers import ElectronicQueueManager
import datetime

class Entrant(models.Model):
    GENDER_CHOICES = [
        ('Ч', 'Чоловік'),
        ('Ж', 'Жінка'),
    ]

    LEVEL_CHOICES = [
        (2, 'Магістр (професійний рівень)'),
        (3, 'Спеціаліст'),
    ]
    last_name = models.CharField(verbose_name="Прізвище", max_length=20)
    name = models.CharField(verbose_name="Ім'я", max_length=20)
    patronymic = models.CharField(verbose_name="По-батькові", max_length=20)
    phone = models.CharField(verbose_name="Телефон", max_length=20)
    email = models.EmailField(unique=True)

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, verbose_name="Стать")
    birth_date = models.DateField(default='1980-01-01', verbose_name="Дата народження")


    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, verbose_name="Кафедра")
    specialty = models.ForeignKey('Specialty', on_delete=models.SET_NULL, null=True, verbose_name="Спеціальність")

    education_form  = models.ForeignKey('EducationForm',  on_delete=models.SET_NULL, null=True,  verbose_name="Форма навчання")
    funding_source = models.ForeignKey('FundingSource',  on_delete=models.SET_NULL, null=True,  verbose_name="Фінансування")

    scientific_advisor = models.CharField(verbose_name="Керівник", max_length=20)
    foreign_language = models.ForeignKey('ForeignLanguage', on_delete=models.SET_NULL, null=True, verbose_name="Іноземна мова")

    university = models.ForeignKey('University', on_delete=models.SET_NULL, null=True, verbose_name="Заклад вищої освіти")
    level = models.IntegerField(default=3, choices=LEVEL_CHOICES, verbose_name="Рівень диплому про вищу освіту")
    diploma = models.CharField(verbose_name="Серія, № диплому", max_length=10)
    diploma_date = models.DateField(default='1980-01-01', verbose_name="Дата в/диплому")
    diploma_specialty = models.CharField(default="000", verbose_name="Спеціальність (в дипломі)", max_length=50)
    diploma_avg = models.DecimalField(max_digits=5, decimal_places=1, default=0.0, verbose_name="Середній бал")
    diploma_with_honors = models.BooleanField(default=False, verbose_name="Диплом з відзнакою")

    military_registered = models.BooleanField(default=False, verbose_name="Перебування на військовому обліку")
    tck = models.CharField(null=True, blank=True, verbose_name="Повна назва РТЦК та СП (РВК)", max_length=100)

    dormitory_accommodation = models.BooleanField(default=False, verbose_name='Потреба у гуртожитку на час складання іспитів')
    approval_notification = models.BooleanField(default=False, verbose_name="Повідомлення для оформлення додаткової відпустки")

    personal_data_processing = models.BooleanField(default=True,  null=False, verbose_name="Згода на обробку персональних даних")

    electronic_queue = models.ForeignKey('ElectronicQueue', on_delete=models.PROTECT, null=True, verbose_name="Електронна черга")

    # верифікація (перевірка документів)
    verified = models.BooleanField(default=False, verbose_name="Веріфіковано")
    who_verified = models.CharField(null=True, blank=True, verbose_name="Хто перевірив відомості", max_length=15)
    notes = models.CharField(null=True, blank=True, verbose_name="Примітки", max_length=255)

    # додаткові вступні випробування
    need_additional_tests = models.BooleanField(default=False, verbose_name="Необхідність у додаткових вступних випробуваннях")
    additional_tests = models.BooleanField(default=False, verbose_name="Додаткові вступні випробування")

    # оцінки
    grade_specialty = models.DecimalField(max_digits=6, decimal_places=2, default=0.0, null=False, blank=False, verbose_name="Оцінка за спеціальність")
    grade_foreign_language = models.DecimalField(max_digits=6, decimal_places=2, default=0.0, null=False, blank=False, verbose_name="Оцінка за іноземну мову")
    grade_scientific_achievements = models.DecimalField(max_digits=6, decimal_places=2, default=0.0, null=True, blank=False, verbose_name="Наукові досягнення")

    competition_score = models.DecimalField(max_digits=6, decimal_places=2, default=0.0, null=False, blank=False, verbose_name="Конкурсний бал")
    recommended = models.BooleanField(default=False, verbose_name="Рекомендовано до зарахування за державним замовленням")

    vidrahovano = models.BooleanField(default=False, verbose_name="Відраховано")

    order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True, verbose_name="Наказ про зарахування")

    studing_group = models.ForeignKey('StudingGroup', on_delete=models.SET_NULL, null=True, verbose_name="Навчальна група")

   # user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    @property
    def is_verified(self):
        return bool(self.verified)

    def clean(self):
        super().clean()

        # Додаємо код країни якщо відсутній
        phone_number = self.phone
        if not phone_number.startswith('+'):
            phone_number = f'+{phone_number}'

        try:
            # Перевірка телефонного номеру перед збереженням
            parsed_number = parse(phone_number, None)
            if not is_valid_number(parsed_number):
                raise ValidationError("Недійсний телефонний номер.")
        except Exception as e:
            raise ValidationError("Помилка перевірки телефонного номеру: %s" % e)

    def __str__(self):
        return f'{self.last_name} {self.name} {self.patronymic}'

    def get_absolute_url(self):
        return reverse('entrant-detail', args=[str(self.id)])


@receiver(post_save, sender=Entrant)
def update_who_verified(sender, instance, created, **kwargs):
    if instance.verified and 'request' in kwargs:
        # Отримуємо інформацію про користувача з аргументів request
        user_who_modified = kwargs['request'].user

        # Встановлюємо логін користувача в поле who_verified
        instance.who_verified = user_who_modified.username
        instance.save()


class University(models.Model):
    name = models.CharField(max_length=255)
    enName = models.CharField(max_length=255)
    shortName = models.CharField(max_length=100)
    educationTypeName = models.CharField(max_length=100)
    financingTypeName = models.CharField(max_length=50)
    location = models.CharField(max_length=20)

    def get_absolute_url(self):
        return reverse('university-detail', args=[str(self.id)])

    def __str__(self):
        return format_output(self.shortName, self.name)
        # return f'{self.shortName} - {self.name}'

    class Meta:
        ordering = ['shortName']

def format_output(short_name, name):
    # Перевірка, чи є значення для обох частин
    if short_name and name:
        formatted_string = f'{short_name} - {name}'
    # Якщо немає name, вивести тільки short_name
    elif short_name:
        formatted_string = short_name
    # Якщо немає short_name, вивести тільки name
    elif name:
        formatted_string = name
    else:
        formatted_string = ''  # Якщо обидві частини пусті

    # Обмежити довжину до 80 символів
    formatted_string = formatted_string[:90]

    return formatted_string


class Faculty(models.Model):
    name = models.CharField(max_length=100)
    shortName = models.CharField(max_length=15)
    def __str__(self):
        return self.shortName
    class Meta:
        ordering = ['shortName']


class Department(models.Model):
    name = models.CharField(max_length=100)
    shortName = models.CharField(max_length=15)

    faculty = models.ForeignKey('Faculty', on_delete=models.PROTECT, null=False, verbose_name="Факультет")
    specialties = models.ManyToManyField('Specialty', help_text="Спеціальність")

    # формування списку спеціальностей, що відносяться до кафедри
    def display_specialty(self):
        return ', '.join([specialty.code for specialty in self.specialties.all() ])
    display_specialty.short_description = 'Спеціальності'

    def __str__(self):
        return f'{self.shortName} - {self.name}'

    class Meta:
        ordering = ['shortName']


class Specialty(models.Model):
    code = models.CharField(max_length=3, default="000")
    name = models.CharField(max_length=100)

    # вивести перелік кафедр, що відносяться до спеціальності
    def display_departments(self):
        return ', '.join([department.shortName for department in Department.objects.filter(specialties=self)])
    display_departments.short_description = 'Кафедри'

    def get_departments(self):
        cath_list = []
        for item in Department.objects.filter(specialties=self):
            cath_list.append(item)
        return cath_list

    def __str__(self):
        return f'{self.code} {self.name}'

    def __str__(self):
        return f'{self.code}'

    class Meta:
        ordering = ['code']


class Onp(models.Model):
    name = models.CharField(max_length=100)
    enName = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=5, decimal_places=1, default=0.0, null=False, blank=False, verbose_name="Обсяг (кредитів)")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class ForeignLanguage (models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class EducationForm (models.Model):
    name = models.CharField(max_length=20)
    shortName = models.CharField(default = "Оч.Денна", max_length=10)
    def __str__(self):
        return self.name

class FundingSource (models.Model):
    name = models.CharField(max_length=100)
    shortName = models.CharField(max_length=10)
    def __str__(self):
        return self.name

class StudingGroup (models.Model):
    name = models.CharField(max_length=10)
    def __str__(self):
        return self.name

class Order (models.Model):
    num = models.IntegerField(null=False)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.num} {self.date}'

class ElectronicQueue(models.Model):
    slot = models.DateTimeField()
    name = models.CharField(max_length=50, blank=True, null=True)

    def formated_slot(self):
        return self.slot.strftime('%d.%m.%Y %H:%M')

    def __str__(self):
        return f"{self.formated_slot()} - {self.name}"
