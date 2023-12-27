from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views import generic
from django.shortcuts import render, get_object_or_404
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Auto, Rezervace
from django.contrib.auth.models import User

# Create your views here.
class HomePageView(generic.ListView):
    template_name = "auta/homepage.html"
    context_object_name = "auta_list"
    def get_queryset(self):
        return Auto.objects.all().order_by('-rok_vyroby')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_popup'] = self.request.GET.get('show_popup', False)
        context['email'] = self.request.GET.get('email', "")
        context['error_message'] = self.request.GET.get('error_message', "")
        return context
    
class DetailView(generic.DetailView):
    model = Auto
    template_name = "auta/detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['aktualni_datum_a_cas'] = datetime.now().strftime('%Y-%m-%dT%H:%M')
        return context
    
def car_view(request, auto_id):
    try:
        auto = Auto.objects.get(pk=auto_id)
    except Auto.DoesNotExist:
        raise Http404("Auto neexistuje")
    return render(request, 'auta/detail.html', {"auto": auto})

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

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get("password")
        try:
            username = User.objects.get(email=email)
        except:
            return HttpResponseRedirect(reverse('auta:homepage') + '?show_popup=True&email=' + email + '&error_message=Neplatné přihlašovací údaje.')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('auta:homepage') + '?error_message=Úspěšně přihlášeno.')
        else:
            return HttpResponseRedirect(reverse('auta:homepage') + '?show_popup=True&email=' + email + '&error_message=Neplatné přihlašovací údaje.')
    
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect(reverse('auta:homepage') + '?error_message=Úspěšně odhlášeno.')




def register(request):
    email = request.POST["email"]
    password = request.POST["password"]
    user = User.objects.create_user(email, email, password)
    if user is not None:
        login(request, user)
        return HttpResponse("Registrace byla úspěšná.")
    else:
        return HttpResponse("Neplatné registrační údaje.")