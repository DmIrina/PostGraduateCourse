Django

deactivate 	— Выход из текущей виртуальной среды Python
workon 		— Список доступных виртуальных сред
workon name_env 		— Активация виртуальной среды Python
rmvirtualenv name_env 	— Удаление виртуальной среды.

pip3 install django
py -m django --version

django-admin startproject pgc .
python manage.py startapp vstup

python manage.py makemigrations
python manage.py migrate

python manage.py runserver
python manage.py createsuperuser


pip install Pillow
pip install django-cleanup


SQL
DELETE FROM vstip_specialty
DELETE FROM vstup_cathedra

DROP TABLE vstip_specialty



# усунути проблеми з міграціями
python manage.py migrate --fake vstup


.venv\scripts\activate

python manage.py makemigrations

python manage.py migrate

python manage.py runserver

таблиці
// pip install django-tables2
в вірт середовищі:  python -m pip install django-tables2
                    python -m pip install pip install django-filter
                    python -m pip install django-bootstrap-v5

додати в INSTALLED_APPS:    django_tables2
                            django-filters                  # тут filters а в пакеті filter
                            bootstrap5
додати 'django.template.context_processors.request' в context_processors в секції налаштувань шаблонів OPTIONS.