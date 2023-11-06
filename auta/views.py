from django.http import HttpResponse
from django.views import generic
from django.shortcuts import render, get_object_or_404
from datetime import datetime, timedelta

from .models import Auto, Rezervace

# Create your views here.
class HomePageView(generic.ListView):
    template_name = "auta/homepage.html"
    context_object_name = "auta_list"
    def get_queryset(self):
        return Auto.objects.all().order_by('-rok_vyroby')
    
class DetailView(generic.DetailView):
    model = Auto
    template_name = "auta/detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['aktualni_datum_a_cas'] = datetime.now().strftime('%Y-%m-%dT%H:%M')
        return context

def reserve(request, auto_id):
    auto = get_object_or_404(Auto, pk = auto_id)
    if request.method == 'POST':
        datum_a_cas = request.POST.get('datum_a_cas')
        if datum_a_cas:
            datum_a_cas = datetime.strptime(datum_a_cas, '%Y-%m-%dT%H:%M')
            
            # Ověříme, zda datum_a_cas není v minulosti.
            if datum_a_cas < datetime.now() + timedelta(minutes=14):
                return render(request, 'auta/detail.html', {'auto': auto, 'error_message': "Rezervace musí být vytvořena alespoň s 15 minutovým předstihem.", 'aktualni_datum_a_cas' : datum_a_cas.strftime('%Y-%m-%dT%H:%M')})
            
            
            # Nastavení pevné otevírací doby
            oteviraci_doba_zacatek = datum_a_cas.replace(hour=8, minute=0, second=0, microsecond=0)
            oteviraci_doba_konec = datum_a_cas.replace(hour=22, minute=0, second=0, microsecond=0)
            
            # Ověříme, zda rezervace spadá do otevírací doby
            if not (oteviraci_doba_zacatek <= datum_a_cas <= oteviraci_doba_konec):
                return render(request, 'auta/detail.html', {'auto': auto, 'error_message': "Rezervace musí být během otevírací doby 8:00 - 22:00.", 'aktualni_datum_a_cas' : datum_a_cas.strftime('%Y-%m-%dT%H:%M')})
            
            # Zjistíme, zda existuje jiná rezervace do 30 minut od požadované rezervace.
            rezervace_30_min_pred = datum_a_cas - timedelta(minutes=30)
            rezervace_30_min_po = datum_a_cas + timedelta(minutes=30)
            
            existujici_rezervace = Rezervace.objects.filter(auto=auto, datum_a_cas__range=(rezervace_30_min_pred, rezervace_30_min_po))
            
            if existujici_rezervace.exists():
                return render(request, 'auta/detail.html', {'auto': auto, 'error_message': "Rezervace v tomto termínu již existuje, vyberte prosím jiný termín.", 'aktualni_datum_a_cas' : datum_a_cas.strftime('%Y-%m-%dT%H:%M')})
            
            rezervace = Rezervace(auto=auto, datum_a_cas=datum_a_cas)
            rezervace.save()
            # Můžete přesměrovat uživatele na stránku s potvrzením nebo jiným vhodným způsobem.
            return HttpResponse(f"Rezervace byla úspěšně vytvořena na {datum_a_cas.strftime('%d.%m.%Y')} v {datum_a_cas.strftime('%H:%M')}")

    # Pokud žádost nebyla metoda POST nebo pokud datum_a_cas nebylo definováno, zobrazte formulář.
    return render(request, 'auta/detail.html', {"auto": auto, "error_message": "Rezervace nebyla provedena.", 'aktualni_datum_a_cas' : datum_a_cas.strftime('%Y-%m-%dT%H:%M')})