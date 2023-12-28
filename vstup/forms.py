from django import forms
from datetime import date, timedelta

from django.forms import ModelForm
from django.urls import reverse
from django.utils.html import format_html

from .models import Specialty, Department, ElectronicQueue, Entrant, EducationForm, FundingSource, University, \
    ForeignLanguage


# форма додавання в БД нових спеціальностей
class Form_add_specialty(forms.Form):
    code = forms.CharField(label="Код")
    name = forms.CharField(label="Назва")


class Form_edit_specialty(forms.ModelForm):
    class Meta:
        model = Specialty
        fields = '__all__'


class DepartmentModelForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'


class EntrantEditForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('Ч', 'Чоловік'),
        ('Ж', 'Жінка'),
    ]

    LEVEL_CHOICES = [
        (2, 'Магістр (професійний рівень)'),
        (3, 'Спеціаліст'),
    ]

    last_name = forms.CharField(max_length=20, required=True, label='Прізвище')
    name = forms.CharField(max_length=20, required=True, label="Ім'я")
    patronymic = forms.CharField(max_length=20, required=True, label='По-батькові')
    phone = forms.CharField(max_length=20, required=True, label='Телефон +380xx1234567')
    email = forms.EmailField(max_length=120, required=True)
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True, label='Стать')
    max_birth_date = date.today() - timedelta(days=365.25 * 20)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'max': max_birth_date}), label='Дата народження')
    specialty = forms.ModelChoiceField(queryset=Specialty.objects.all(), required=True, label='Спеціальність, за якою вступаєте до аспірантури')  #
    education_form = forms.ModelChoiceField(queryset=EducationForm.objects.all(), required=True, label='Форма навчання')  #
    funding_source = forms.ModelChoiceField(queryset=FundingSource.objects.all(), required=True, label='Джерело фінансування (очна форма)')  #
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=True, label='Кафедра')  #

    scientific_advisor = forms.CharField(max_length=20, required=True, label='Прізвище передбачуваного наукового керівника')  #
    foreign_language = forms.ModelChoiceField(queryset=ForeignLanguage.objects.all(), required=True, label='Іноземна мова (вступний іспит)')  #
    university = forms.ModelChoiceField(queryset=University.objects.all(), required=True, label='Заклад вищої освіти')  #
    level = forms.ChoiceField(choices=LEVEL_CHOICES, required=True, label='Рівень диплому про вищу освіту')  #

    diploma = forms.CharField(max_length=10, required=True, label='Серія, № диплому')  #
    diploma_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'max': date.today()}), label='Дата отримання диплому')
    diploma_specialty = forms.CharField(max_length=50, required=True, label='Код та назва спеціальності, зазначені в дипломі')  #
    diploma_avg = forms.DecimalField(max_digits=5, decimal_places=1, required=True, label='Середній бал диплому')  #
    diploma_with_honors = forms.BooleanField(required=False, label='Диплом з відзнакою')  #
    military_registered = forms.BooleanField(required=False, label='Перебування на військовому обліку')  #
    tck = forms.CharField(max_length=100, required=False, label='Повна назва РТЦК та СП (РВК)')  #
    dormitory_accommodation = forms.BooleanField(required=False, label='Потреба у гуртожитку на час складання іспитів')  #
    approval_notification = forms.BooleanField(required=False, label='Повідомлення для оформлення додаткової відпустки')  #
    electronic_queue = forms.ModelChoiceField(queryset=ElectronicQueue.objects.all(), required=True, label='Електронна черга')  #
    personal_data_processing = forms.BooleanField(required=True, label='Згода на обробку персональних даних')  #


    class Meta:
        model = Entrant
        fields = ['last_name', 'name', 'patronymic', 'phone', 'email',
                  'gender', 'birth_date',
                  'specialty', 'education_form', 'funding_source', 'department', 'scientific_advisor',
                  'foreign_language',
                  'university', 'level', 'diploma', 'diploma_date', 'diploma_specialty', 'diploma_avg',
                  'diploma_with_honors',
                  'military_registered', 'tck',
                  'dormitory_accommodation', 'approval_notification', 'personal_data_processing',
                  'electronic_queue']


class EntrantVerifyForm(EntrantEditForm):
    need_additional_tests = forms.BooleanField(required=False, label='Необхідність у додаткових випробуваннях')
    verified = forms.BooleanField(label='Відомості перевірено')
    who_verified = forms.CharField(label='Хто перевірив відомості')
    notes = forms.CharField(widget=forms.Textarea, required=False, label='Примітки')

    class Meta:
        model = Entrant
        fields = ['last_name', 'name', 'patronymic', 'phone', 'email',
                  'gender', 'birth_date',
                  'specialty', 'education_form', 'funding_source', 'department', 'scientific_advisor',
                  'foreign_language',
                  'university', 'level', 'diploma', 'diploma_date', 'diploma_specialty', 'diploma_avg',
                  'diploma_with_honors',
                  'military_registered', 'tck',
                  'dormitory_accommodation', 'approval_notification',
                  'need_additional_tests', 'verified', 'who_verified', 'notes'
                  ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['electronic_queue']
        del self.fields['personal_data_processing']


class EntrantAddtestForm(forms.ModelForm):
    last_name = forms.CharField(max_length=20, required=False, label='Прізвище', widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    name = forms.CharField(max_length=20, required=False, label="Ім'я", widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    patronymic = forms.CharField(max_length=20, required=False, label='По-батькові', widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    specialty = forms.ModelChoiceField(queryset=Specialty.objects.all(), required=True, label='Спеціальність')
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=True, label='Кафедра')
    additional_tests = forms.BooleanField(required=False, label='Додаткові вступні випробування')

    # додати кнопку Cansel
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields[''] = forms.CharField(
    #         widget=forms.TextInput(attrs={'class': 'btn btn-secondary', 'value': 'Cancel', 'id': 'id_cancel', 'href' : 'index'}),
    #         required=False,
    #         initial='Cancel'
    #     )

    class Meta:
        model = Entrant
        fields = ['last_name', 'name', 'patronymic', 'specialty', 'department', 'additional_tests']

#
class EntrantGradesForm(forms.ModelForm):
    last_name = forms.CharField(max_length=20, required=False, label='Прізвище', widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    name = forms.CharField(max_length=20, required=False, label="Ім'я", widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    patronymic = forms.CharField(max_length=20, required=False, label='По-батькові', widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    specialty = forms.ModelChoiceField(queryset=Specialty.objects.all(), required=True, label='Спеціальність')
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=True, label='Кафедра')
    grade_specialty = forms.DecimalField(max_digits=6, decimal_places=2, required=False, label='Оцінка за спеціальність')
    grade_foreign_language = forms.DecimalField(max_digits=6, decimal_places=2, required=False, label='Оцінка за іноземну мову')
    grade_scientific_achievements = forms.DecimalField(max_digits=6, decimal_places=2, required=False, label='Наукові досягнення')
    competition_score = forms.DecimalField(max_digits=6, decimal_places=2, required=False, label='Конкурсний бал')
    recommended = forms.BooleanField(required=False, label='Рекомендований')
    class Meta:
        model = Entrant
        fields = ['last_name', 'name', 'patronymic', 'specialty', 'department',
                               'grade_specialty', 'grade_foreign_language', 'grade_scientific_achievements',
                               'competition_score', 'recommended']

class CompetitionScoreForm(forms.Form):
    a = forms.DecimalField(max_digits=4, decimal_places=2, label='Спец', required=True)
    b = forms.DecimalField(max_digits=4, decimal_places=2, label='Іноз', required=True)
    c = forms.DecimalField(max_digits=4, decimal_places=2, label='Досяг', required=True)

class EQueueForm(forms.Form):
    start_date = forms.DateField(widget=forms.SelectDateWidget)
    end_date = forms.DateField(widget=forms.SelectDateWidget)
    launch_hour = forms.ChoiceField(choices=[(hour, f'{hour:02}:00') for hour in range(24)])
    work_hours = forms.MultipleChoiceField(choices=[(hour, f'{hour:02}:00') for hour in range(24)], widget=forms.CheckboxSelectMultiple)
    weekends = forms.MultipleChoiceField(choices=[(day, day_name) for day, day_name in enumerate(['Понеділок', 'Вівторок', 'Середа', 'Четвер', "П'ятниця", 'Субота', 'Неділя'])], widget=forms.CheckboxSelectMultiple)


class EntrantModelForm(forms.ModelForm):
    class Meta:
        model = Entrant
        fields = '__all__'


class UniverForm(forms.ModelForm):
    class Meta:
        model = University
        fields = '__all__'

#
# class UniverForm(forms.ModelForm):
#     class Meta:
#         model = University
#         fields = ['name', 'enName', 'shortName', 'educationTypeName', 'financingTypeName', 'location']
#         widgets = { 'name': forms.TextInput(attrs={ 'class': 'form-control' }),
#                     'enName': forms.TextInput(attrs={'class': 'form-control'}),
#                     'shortName': forms.TextInput(attrs={'class': 'form-control'}),
#                     'educationTypeName': forms.TextInput(attrs={'class': 'form-control'}),
#                     'financingTypeName': forms.TextInput(attrs={'class': 'form-control'}),
#                     'location': forms.TextInput(attrs={'class': 'form-control'})
#       }
