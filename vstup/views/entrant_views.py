from django.shortcuts import redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, DeleteView
from django.http import JsonResponse
from ..models import Entrant, ElectronicQueue
from ..forms import EntrantEditForm, EntrantVerifyForm, EntrantAddtestForm, EntrantGradesForm, CompetitionScoreForm
from django.db.models import Q

# всі вступники, що зареєструвалися
def primary_info_list(request):
    primary_info_list = Entrant.objects.all()
    context = {'primary_info_list': primary_info_list}
    return render(request, "vstup/primary_info_list.html", context)


class PrimaryInfoCreate(CreateView):
    model = Entrant
    success_url = reverse_lazy('primary_info_list')
    template_name = 'vstup/primary_info_form.html'

    def get(self, request, *args, **kwargs):
        form = EntrantEditForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = EntrantEditForm(data=request.POST)
        if form.is_valid():
            electronic_queue = form.cleaned_data['electronic_queue']
            entrant = form.save()

            context = {
                'form': form,
                'eq': electronic_queue.slot.strftime('%d.%m.%Y %H:%M'),
                'success_message': 'Реєстраційні дані успішно збережено'
            }

            print(electronic_queue.slot)

            electronic_queue.name = f'{entrant.last_name} {entrant.name} {entrant.patronymic}'
            electronic_queue.save()

            return render(request, 'vstup/entrant_success_modal.html', context)
        return render(request, self.template_name, {'form': form})


class ShowSuccessModalView(SuccessMessageMixin, TemplateView):
    template_name = 'vstup/entrant_success_modal.html'
    success_message = 'Entrant successfully added!'


@method_decorator(csrf_exempt, name='dispatch')
class EntrantEditView(View):
    template_name = 'vstup/primary_info_form.html'

    def get(self, request, pk, *args, **kwargs):
        entrant = get_object_or_404(Entrant, pk=pk)
        form = EntrantEditForm(instance=entrant)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk, *args, **kwargs):
        entrant = get_object_or_404(Entrant, pk=pk)
        form = EntrantEditForm(data=request.POST, instance=entrant)

        if form.is_valid():
            electronic_queue = form.cleaned_data['electronic_queue']
            if electronic_queue.name == 'Free':
                entrant_old = Entrant.objects.get(id=entrant.id)
                try:
                    equeue_old = ElectronicQueue.objects.get(id=entrant_old.electronic_queue_id)
                    equeue_old.name = 'Free'
                    equeue_old.save()
                except Exception as e:
                    print(e)

                form.save()

                electronic_queue.name = f'{entrant.last_name} {entrant.name} {entrant.patronymic}'
                electronic_queue.save()

                return JsonResponse({'status': 'success', 'redirect_url': self.success_url})

        # Поверніть помилки форми в разі невдалий валідації
        return JsonResponse({'status': 'error', 'errors': form.errors})


#
class EntrantEdit(View):
    success_url = reverse_lazy('primary_info_list')
    template_name = 'vstup/primary_info_form.html'

    def get(self, request, pk, *args, **kwargs):
        entrant = get_object_or_404(Entrant, pk=pk)
        form = EntrantEditForm(instance=entrant)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk, *args, **kwargs):
        entrant = get_object_or_404(Entrant, pk=pk)
        form = EntrantEditForm(data=request.POST, instance=entrant)

        if form.is_valid():
            # Костиль - в електронній черзі звільняє поле Name старе та записує нове
            electronic_queue = form.cleaned_data['electronic_queue']
            if electronic_queue.name == 'Free':
                entrant_old = Entrant.objects.get(id=entrant.id)
                try:
                    equeue_old = ElectronicQueue.objects.get(id=entrant_old.electronic_queue_id)
                    equeue_old.name = 'Free'
                    equeue_old.save()
                except Exception as e:
                    print(e)

                form.save()

                electronic_queue.name = f'{entrant.last_name} {entrant.name} {entrant.patronymic}'
                electronic_queue.save()

                return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})


class EntrantDelete(DeleteView):
    model = Entrant
    success_url = reverse_lazy('primary_info_list')

# *************                   Верифікація                *************
# список вступників, що пройшли верифікацію
def entrant_verified_list(request):
    list = Entrant.objects.filter(verified=True)
    context = {'list': list}
    return render(request, "vstup/entrant_verified_list.html", context)

class EntrantVerify(UpdateView):
    model = Entrant
    form_class = EntrantVerifyForm
    success_url = reverse_lazy('primary_info_list')
    template_name = 'vstup/entrant_verify.html'


class EntrantVerifiedEdit(UpdateView):
    model = Entrant
    form_class = EntrantVerifyForm
    success_url = reverse_lazy('entrant_verified_list')
    template_name = 'vstup/entrant_verify.html'


#  ************** Відмітити тих, що здали додаткові іспити *************
# список вступників, що потребують додаткових іспитів
def entrant_addtest_list(request):
    context = {}                    # заповнюється ajax запитом від клієнта до entrants_addtest_json
    return render(request, 'vstup/datatable/entrant_addtest_list.html', context)

# викликаємо з клієнта запитом Ajax - у списку лише ті, що потребують додатк іспиту
def entrants_addtest_json(request):
    result_list = list(Entrant.objects.filter(need_additional_tests=True).values('last_name', 'name', 'patronymic',
                                                    'specialty__code', 'department__shortName', 'additional_tests', 'id'))
    # Повернути відповідь JSON
    return JsonResponse(result_list, safe=False)

class EntrantAddtestEdit(UpdateView):
    model = Entrant
    form_class = EntrantAddtestForm
    success_url = reverse_lazy('entrant_addtest_list')


# *************          Виставити оцінки           *************

def entrant_grades_list(request):
    form = CompetitionScoreForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        a = form.cleaned_data['a']
        b = form.cleaned_data['b']
        c = form.cleaned_data['c']
        print(a, b, c)
        entrants = Entrant.objects.all()
        for entrant in entrants:
            # Assuming you have fields grade_specialty, grade_foreign_language, grade_scientific_achievements
            competition_score = a * entrant.grade_specialty + b * entrant.grade_foreign_language + c * entrant.grade_scientific_achievements
            print(entrant.last_name, competition_score)
            # Update the competition_score field in the database
            entrant.competition_score = competition_score
            entrant.save()
        return redirect('entrant_grades_list')
    context = {'form': form}
    return render(request, 'vstup/datatable/entrant_grades_list.html', context)


# у списку лише ті, що допущені до іспитів: верифіковані та кому необхідно - склали додатк іспит
def entrants_grades_json(request):
    result_list = list(Entrant.objects.filter((Q(verified=True, need_additional_tests=False)) |
                                              (Q(verified=True, need_additional_tests=True, additional_tests=True)))
                       .values('last_name', 'name', 'patronymic', 'specialty__code', 'department__shortName',
                               'grade_specialty', 'grade_foreign_language', 'grade_scientific_achievements',
                               'competition_score', 'competition_score', 'recommended', 'id'))
    # Повернути відповідь JSON
    return JsonResponse(result_list, safe=False)


class EntrantGradesEdit(UpdateView):
    model = Entrant
    form_class = EntrantGradesForm
    success_url = reverse_lazy('entrant_grades_list')

# entrant_table
def entrant_table(request):
    context = {}                    # заповнюється ajax запитом від клієнта
    return render(request, 'vstup/datatable/entrant_table.html', context)


def entrants_json(request):
    result_list = list(Entrant.objects.all().values('last_name', 'name', 'patronymic', 'phone', 'email', 'id', ))
    return JsonResponse(result_list, safe=False)


class EntrantUpdate(UpdateView):
    model = Entrant
    fields = '__all__'
    success_url = reverse_lazy('entrant_table')

