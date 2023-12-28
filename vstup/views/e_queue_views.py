from django.contrib import messages
from django.db.models import ProtectedError
from django.http import HttpResponseServerError
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.db import IntegrityError
import datetime
from ..models import ElectronicQueue
from ..forms import EQueueForm


# from django.shortcuts import render
# from django.views.generic import ListView, DetailView, View
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
# from django.http import HttpResponse
# from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from django.urls import reverse_lazy, reverse
# from ..forms import Form_edit_specialty, Form_add_specialty, EntrantEditForm

def equeue_list(request):
    equeue = ElectronicQueue.objects.all()
    context = {'equeue': equeue}
    return render(request, "vstup/equeue_list.html", context)


def equeue_refresh(request):
    unrelated_objects = ElectronicQueue.objects.filter(entrant__isnull=True)

    try:
        unrelated_objects.delete()
    except IntegrityError:
        pass

    equeue = ElectronicQueue.objects.all()
    context = {'equeue': equeue}
    return render(request, "vstup/equeue_list.html", context)


def equeue_new(request):
    if request.method == 'POST':
        form = EQueueForm(request.POST)
        if form.is_valid():
            print("POST - valid")
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            work_hours = form.cleaned_data['work_hours']
            launch_hour = form.cleaned_data['launch_hour']
            weekends = form.cleaned_data['weekends']

            # Bulk create ElectronicQueue entries
            equeue_objects = []
            for day in range((end_date - start_date).days + 1):
                current_date = start_date + datetime.timedelta(days=day)
                if current_date.weekday() not in weekends:
                    for hour_str in work_hours:
                        hour = int(hour_str)
                        if hour != launch_hour:
                            for minute in range(0, 60, 15):
                                timing_datetime = datetime.datetime.combine(current_date, datetime.time(hour, minute))
                                eq = timezone.make_aware(timing_datetime, timezone.get_current_timezone())
                                equeue_objects.append(ElectronicQueue(slot=eq, name='Free'))

            ElectronicQueue.objects.bulk_create(equeue_objects)

            return redirect('equeue_list')  # Redirect to the queue list page after creating the queue
        else:
            print("POST - invalid")
    else:
        print("- GET ")
        form = EQueueForm()

    context = {'form': form}
    return render(request, 'vstup/equeue_new.html', context)


class ElectrinicQueueUpdate(UpdateView):
    model = ElectronicQueue
    fields = '__all__'
    success_url = reverse_lazy('equeue_list')


class ElectrinicQueueDelete(DeleteView):
    model = ElectronicQueue
    success_url = reverse_lazy('equeue_list')
