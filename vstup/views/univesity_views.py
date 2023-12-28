from django.shortcuts import render, redirect,  get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django_tables2 import RequestConfig

from ..filters import UniversityFilter
from ..tables import UniversityTable
from ..forms import UniverForm

from ..models import University


def universities_edit(request):
    universities = University.objects.all()
    context = {'universities': universities}
    return render(request, "vstup/universities_edit.html", context)


class UniversityCreate(CreateView):
    model = University
    fields = '__all__'
    success_url = reverse_lazy('universities_edit')




class UniversityDelete(DeleteView):
    model = University
    success_url = reverse_lazy('universities_edit')


def university_list(request):
    queryset = University.objects.all()
    table = UniversityTable(queryset)
    filter = UniversityFilter(request.GET, queryset=queryset)
    RequestConfig(request, paginate={'per_page': 10}).configure(table)  # Застосувати конфігурацію до таблиці
    return render(request, 'vstup/bootstrap_django_tables.html', {'table': table, 'filter': filter})


def addnewuniver(request):
    if request.method == "POST":
        form = UniverForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/')
            except:
                pass
    else:
        form = UniverForm()
    return render(request, 'vstup/univer/indexuniver.html', {'form': form})


def indexuniver(request):
    univerlist = University.objects.all()
    return render(request, "vstup/univer/showuniver.html", {'univerlist': univerlist})


def edituniver(request, id):
    univer = University.objects.get(id=id)
    return render(request, 'vstup/univer/edituniver.html', {'univer': univer})


class UniversityUpdate(UpdateView):
    model = University
    fields = '__all__'
    success_url = reverse_lazy('universities_edit')


class UpdateUniver(UpdateView):
    model = University
    fields = '__all__'
    success_url = reverse_lazy('indexuniver')

# def updateuniver(request, id):
#     univer = University.objects.get(id=id)
#     print(univer.name)
#     form = UniverForm(request.POST, instance=univer)
#     if form.is_valid():
#         form.save()
#         print(univer.name + " - valid - ")
#         return redirect("/indexuniver")
#     print(univer.name + " - NO valid - ")
#     return render(request, 'vstup/univer/edituniver.html', {'univer': univer})


def destroy(request, id):
    univer = University.objects.get(id=id)
    univer.delete()
    return redirect("/")