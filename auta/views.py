from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

from .models import Auto

# Create your views here.
class HomePageView(generic.ListView):
    template_name = "auta/homepage.html"
    context_object_name = "auta_list"
    def get_queryset(self):
        return Auto.objects.all()