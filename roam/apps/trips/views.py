from django.shortcuts import render
from django.views import generic

from .models import Trip

# Create your views here.
class IndexView(generic.ListView):
    model = Trip
    template_name = 'trips/index.html'
    context_object_name = 'trips'
    ordering = ['-start_date']

