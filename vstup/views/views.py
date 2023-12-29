from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

from ..models import Entrant, ElectronicQueue, University, Faculty, Department, Specialty
from ..forms import Form_edit_specialty, Form_add_specialty, EntrantEditForm


def index(request):
    # Словник для передачі даних у шаблон

    text_head = 'Вступ до аспірантури'
    text_body = 'Загальні положення'

    num_entrants = Entrant.objects.all().count()
    num_military = Entrant.objects.filter(military_registered=True).count()

    context = {
        'text_head': text_head,
        'text_body': text_body,
        'num_entrants': num_entrants,
        'num_military': num_military
    }

    # nередача словаря context з даними до шаблону
    return render(request, 'vstup/index.html', context)


class EntrantListView(ListView):
    model = Entrant
    paginate_by = 40
    context_object_name = 'entrants'
    # template_name - шаблон  (за замовченням - entrant_list.html) - перевизначення: template_name = 'my_entrant_list.html'
    # context_object_name - список з БД, назва змінної в шаблоні (за замовченням - object_list)
    # queryset = Entrant.objects.filter(name__icontains='Сідоренко')[:5] # отримати 5 записів із словом 'Петро' в імені


class EntrantDetailView(DetailView):
    model = Entrant

class SpecialtyListView(ListView):
    model = Specialty
    paginate_by = 10
    context_object_name = 'specialties'


class SpecialtyDetailView(DetailView):
    model = Specialty


class CathedraListView(ListView):
    model = Department
    paginate_by = 10
    context_object_name = 'departments'


class CathedraDetailView(DetailView):
    model = Department

class EntrantFullListView(LoginRequiredMixin, ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = Entrant
    template_name = 'vstup/entrant_full_list.html'
    paginate_by = 40


def about(request):
    text_head = 'Про нас'
    name = 'Відділ аспірантури та докторантури КПІ ім. Ігоря Сікорського'
    rab1 = 'Навчання аспірантів та докторантів'
    rab2 = 'Підготовка наукових та науково-педагогічних кадрів'
    rab3 = 'Ведення обліків аспірантів та докторантів'
    rab4 = 'Інше'
    context = {'text_head': text_head, 'name': name,
               'rab1': rab1, 'rab2': rab2,
               'rab3': rab3, 'rab4': rab4}
    # передача словаря context с данными в шаблон
    return render(request, 'vstup/about.html', context)


def contact(request):
    text_head = 'Контакти'
    name = 'Відділ аспірантури та докторантури КПІ ім. Ігоря Сікорського'
    address = 'Київ, Берестейський просп. 37, корп. 1, к. 247'
    tel = '+38-044-2049349'
    email = 'aspirantura@kpi.ua'
    # Словарь для передачи данных в шаблон index.html
    context = {'text_head': text_head,
               'name': name, 'address': address,
               'tel': tel,
               'email': email}
    # передача словаря context с данными в шаблон
    return render(request, 'vstup/contact.html', context)


# виклик сторінки редагування спеціальностей
def specialties_edit(request):
    specialty = Specialty.objects.all()
    context = {'specialty': specialty}
    return render(request, "vstup/specialties_edit.html", context)


# Створення нової спеціальності в БД
def specialty_add(request):
    if request.method == 'POST':
        form = Form_add_specialty(request.POST, request.FILES)
        if form.is_valid():
            # отримати дані з форми
            code = form.cleaned_data.get("code")
            name = form.cleaned_data.get("name")
            # створити об'єкт для запису в БД
            obj = Specialty.objects.create(
                code=code,
                name=name)
            obj.save()  # зберегти отримані дані
            return HttpResponseRedirect(reverse('specialties_edit'))  # завантажити сторінку зі списком
    else:
        form = Form_add_specialty()
        context = {"form": form}
        return render(request, "vstup/specialty_add.html", context)


def specialty_delete(request, id):
    try:
        specialty = Specialty.objects.get(id=id)
        specialty.delete()
        return HttpResponseRedirect("/specialties_edit/")
    except:
        return HttpResponseNotFound("<h2>Спеціальність не знайдено</h2>")


def specialty_edit(request, id):
    author = Specialty.objects.get(id=id)
    # specialty = get_object_or_404(Specialty, pk=id)
    if request.method == "POST":
        instance = Specialty.objects.get(pk=id)
        form = Form_edit_specialty(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/specialties_edit/")
    else:
        form = Form_edit_specialty(instance=author)
        content = {"form": form}
        return render(request, "vstup/specialty_edit.html", content)


def departments_edit(request):
    departments = Department.objects.all()
    context = {'departments': departments}
    return render(request, "vstup/departments_edit.html", context)


class DepartmentCreate(CreateView):
    model = Department
    fields = '__all__'
    success_url = reverse_lazy('departments_edit')


class DepartmentUpdate(UpdateView):
    model = Department
    fields = '__all__'
    success_url = reverse_lazy('departments_edit')


class DepartmentDelete(DeleteView):
    model = Department
    success_url = reverse_lazy('departments_edit')



