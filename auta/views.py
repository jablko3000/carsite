from django.http import HttpResponse
from django.views import generic
from django.shortcuts import render, get_object_or_404
from datetime import datetime, date

from .models import Auto

# Create your views here.
class HomePageView(generic.ListView):
    template_name = "auta/homepage.html"
    context_object_name = "auta_list"
    def get_queryset(self):
        return Auto.objects.all()
    
class DetailView(generic.DetailView):
    model = Auto
    template_name = "auta/detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dnesni_datum'] = date.today()
        context['aktualni_cas'] = datetime.now().time()
        return context

def reserve(request, auto_id):
    auto = get_object_or_404(Auto, pk = auto_id)
    return HttpResponse("Úspěšně rezervováno")