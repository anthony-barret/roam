from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .models import Trip, TripForm


# Create your views here.

class TripIndexView(generic.ListView):
    model = Trip
    template_name = 'trips/index.html'
    context_object_name = 'trips'
    ordering = ['-start_date']


class TripCreateView(generic.CreateView):
    model = Trip
    form_class = TripForm
    template_name = 'trips/create.html'

    def get_success_url(self):
        return reverse_lazy(
            'trips:detail',
            kwargs={'pk': self.object.pk},
        )


class TripDetailView(generic.DetailView):
    model = Trip
    template_name = 'trips/detail.html'
    context_object_name = 'trip'


class TripUpdateView(generic.UpdateView):
    model = Trip
    form_class = TripForm
    template_name = 'trips/update.html'
    context_object_name = 'trip'

    def get_success_url(self):
        return reverse_lazy(
            'trips:detail',
            kwargs={'pk': self.object.pk},
        )


class TripDeleteView(generic.DeleteView):
    model = Trip
    template_name = 'trips/delete.html'
    context_object_name = 'trip'
    success_url = reverse_lazy('trips:index')


def map_page(request):
    return render(request, 'trips/map.html')


def map_data(request):
    codes = Trip.objects.values_list("country__code", flat=True).distinct()
    return JsonResponse({
        "visited_countries": list(codes)
    })
