from django.urls import path

from vstup.views.e_queue_views import equeue_list, equeue_refresh, equeue_new, ElectrinicQueueUpdate, \
    ElectrinicQueueDelete
from vstup.views.entrant_views import primary_info_list, PrimaryInfoCreate, EntrantEdit, EntrantEditView, EntrantDelete, \
    ShowSuccessModalView, EntrantVerify, entrant_verified_list, entrant_table, EntrantUpdate, entrants_json, \
    entrant_addtest_list, EntrantVerifiedEdit, entrants_addtest_json, EntrantAddtestEdit, entrant_grades_list, \
    entrants_grades_json, EntrantGradesEdit
from vstup.views.univesity_views import university_list, universities_edit, UniversityCreate, UniversityDelete, \
    UniversityUpdate, indexuniver, addnewuniver, edituniver, destroy, UpdateUniver
from vstup.views.views import about, contact, index, CathedraListView, CathedraDetailView, SpecialtyListView, \
    SpecialtyDetailView, EntrantFullListView, specialties_edit, specialty_add, specialty_delete, specialty_edit, \
    departments_edit, DepartmentCreate, DepartmentUpdate, DepartmentDelete

urlpatterns = [
    # статичні сторінки
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),

    path('', index, name='index'),

    path('departments/', CathedraListView.as_view(), name='departments'),
    path('departments/<int:pk>', CathedraDetailView.as_view(), name='departments-detail'),

    path('specialties/', SpecialtyListView.as_view(), name='specialties'),
    path('specialties/<int:pk>', SpecialtyDetailView.as_view(), name='specialties-detail'),

    path('specialties_edit/', specialties_edit, name='specialties_edit'),
    path('specialty_add/', specialty_add, name='specialty_add'),
    path('specialty_edit/<int:id>', specialty_edit, name='specialty_edit'),
    path('specialty_delete/<int:id>', specialty_delete, name='specialty_delete'),

    path('departments_edit/', departments_edit, name='departments_edit'),
    path('department/create/', DepartmentCreate.as_view(), name='department_create'),
    path('department/update/<int:pk>/', DepartmentUpdate.as_view(), name='department_update'),
    path('department/delete/<int:pk>/', DepartmentDelete.as_view(), name='department_delete'),

    path('university_list/', university_list, name='university_list'),
    path('universities_edit/', universities_edit, name='universities_edit'),
    path('university/create/', UniversityCreate.as_view(), name='university_create'),
    path('university/update/<int:pk>/', UniversityUpdate.as_view(), name='university_update'),
    path('university/delete/<int:pk>/', UniversityDelete.as_view(), name='university_delete'),

    # Обробка реєстраційних відомостей
    path('primary_info_list/', primary_info_list, name='primary_info_list'),
    path('primary_info_create', PrimaryInfoCreate.as_view(), name='primary_info_create'),
    path('primary_info/update/<int:pk>/', EntrantEdit.as_view(), name='primary_info_update'),
    #  наче 2 однакові
    path('primary_info_edit/<int:pk>/', EntrantEditView.as_view(), name='primary_info_edit'),
    path('primary_info/delete/<int:pk>/', EntrantDelete.as_view(), name='primary_info_delete'),
    path('primary_info_success/', ShowSuccessModalView.as_view(), name='primary_info_success'),

    path('entrant_verify/<int:pk>/', EntrantVerify.as_view(), name='entrant_verify'),
    path('entrantsfull/', EntrantFullListView.as_view(), name='entrants-full'),

    # Верифіковані вступники
    path('entrant_verified_list/', entrant_verified_list, name='entrant_verified_list'),

    # редагування даних верифікованих вступників
    path('entrant_verified_edit/<int:pk>/', EntrantVerifiedEdit.as_view(), name='entrant_verified_edit'),


    # entrant data_table - заготовка для всіх списків вступників (потим можна видалити?)
    path('entrant_table/', entrant_table, name='entrant_table'),
    path('entrant/update/<int:pk>/', EntrantUpdate.as_view(), name='entrant_update'),

    # Додаткові іспити
    path('entrant_addtest_list/', entrant_addtest_list, name='entrant_addtest_list'),
    path('entrants_addtest_json', entrants_addtest_json, name='entrants_addtest_json'),
    # відмітка про складання додаткового іспиту
    path('entrant_addtest_edit/<int:pk>/', EntrantAddtestEdit.as_view(), name='entrant_addtest_edit'),

    # Вступні іспити
    path('entrant_grades_list/', entrant_grades_list, name='entrant_grades_list'),
    path('entrants_grades_json/', entrants_grades_json, name='entrants_grades_json'),
    path('entrant_grades_edit/<int:pk>/', EntrantGradesEdit.as_view(), name='entrant_grades_edit'),



    path('entrants_json', entrants_json, name='entrants_json'),



    path('entrant_verified_list/', entrant_verified_list, name='entrant_verified_list'),

    # path('entrants', entrants, name='entrants'),

    # path('get_entrants/', get_entrants, name='get_entrants'),



# E_QUEUE
    path('equeue_list/', equeue_list, name='equeue_list'),
    path('equeue_refresh/', equeue_refresh, name='equeue_refresh'),
    path('equeue_new/', equeue_new, name='equeue_new'),
    path('equeue/update/<int:pk>/', ElectrinicQueueUpdate.as_view(), name='equeue_update'),
    path('equeue/delete/<int:pk>/', ElectrinicQueueDelete.as_view(), name='equeue_delete'),


# UNIVER
    path('indexuniver', indexuniver, name='indexuniver'),
    path('addnewuniver', addnewuniver, name='addnewuniver'),
    path('edituniver/<int:id>', edituniver, name='edituniver'),
    path('univer/update/<int:pk>/', UpdateUniver.as_view(), name='updateuniver'),
    path('deleteuniver/<int:id>', destroy, name='destroy'),


]
