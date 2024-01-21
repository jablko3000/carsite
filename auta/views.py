from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from datetime import time, timedelta, date
from django.utils import timezone
from django.contrib import messages

from .models import Auto, Rezervace, CustomUser, Image, Note
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def homepage_view(request):
    auta_list = Auto.objects.all().order_by('-datum_nabidky')
    show_popup = request.GET.get('show_popup', False)
    email = request.GET.get('email', "")
    error_message = request.GET.get('error_message', "")
    register = request.GET.get('register', False)
    login = request.GET.get('login', False)

    for auto in auta_list:
        auto.images = Image.objects.filter(auto_id=auto.id).order_by('order')
        auto.notes = Note.objects.filter(auto_id=auto.id).order_by('order')

    context = {
        'auta_list': auta_list,
        'show_popup': show_popup,
        'email': email,
        'error_message': error_message,
        'register': register,
        'login': login,
    }

    return render(request, 'auta/homepage.html', context)

def detail_view(request, auto_id):
    try:
        auto = Auto.objects.get(pk=auto_id)
    except Auto.DoesNotExist:
        raise Http404("Auto neexistuje")
    auto.images = Image.objects.filter(auto_id=auto.id).order_by('order')
    dates = []
    for i in range(7):
        potential_date = date.today() + timedelta(days=i)
        if potential_date.weekday() < 5:
            time_slots = get_time_slots(potential_date, auto)
            if time_slots:
                dates.append(potential_date)

    context = {
        'auto': auto,
        'auto.images': auto.images,
        'dates': dates,
    }
    return render(request, 'auta/detail.html', context)

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Úspěšně přihlášeno.')
            return HttpResponseRedirect(reverse('auta:homepage'))
        else:
            messages.error(request, 'Neplatné přihlašovací údaje.')
            return HttpResponseRedirect(reverse('auta:homepage') + '?show_popup=True&email=' + email + '&login=True')
    else:
        messages.error(request, 'Neznámá chyba.')
        return HttpResponseRedirect(reverse('auta:homepage') + '?login=True')
    
@login_required
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'Úspěšně odhlášeno.')
        return HttpResponseRedirect(reverse('auta:homepage'))
    else:
        messages.error(request, 'Nepodařilo se odhlásit se.')
        return HttpResponseRedirect(reverse('auta:homepage') + '?logout=True')

def user_register(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        if not email or not password1 or not password2 or not full_name or not phone:
            messages.error(request, 'Neplatné přihlašovací údaje.')
            return HttpResponseRedirect(reverse('auta:homepage') + '?show_popup=True&register=True')
        if password1 != password2:
            messages.error(request, 'Hesla se neshodují.')
            return HttpResponseRedirect(reverse('auta:homepage') + '?show_popup=True&register=True')
        else:
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'Uživatel s tímto emailem již existuje.')
                return HttpResponseRedirect(reverse('auta:homepage') + '?show_popup=True&register=True')
            else:
                user = CustomUser.objects.create_user(email, password1, phone, full_name)
                user.save()
                login(request, user)
                messages.success(request, 'Úspěšně zaregistrováno.')
                return HttpResponseRedirect(reverse('auta:homepage'))
    else:
        messages.error(request, 'Nepodařilo se zaregistrovat.')
        return HttpResponseRedirect(reverse('auta:homepage') + '?register=True')

@login_required
def user_profile(request):
    user = request.user
    rezervace = Rezervace.objects.filter(user=user).order_by('-datum_a_cas')
    context = {
        'user': user,
        'rezervace': rezervace,
    }
    return render(request, 'auta/user_profile.html', context)

@login_required
def user_profile_edit(request):
    user = request.user
    if request.method == 'POST':
        form_type = request.POST.get("form_type")
        if form_type == "name":
            full_name = request.POST.get("full_name")
            if not full_name:
                return HttpResponseRedirect(reverse('auta:user_profile') + '?error_message=Neplatné údaje.')
            else:
                user.full_name = full_name
                user.save()
        elif form_type == "email":
            email = request.POST.get("email")
            if not email:
                return HttpResponseRedirect(reverse('auta:user_profile') + '?error_message=Neplatné údaje.')
            else:
                user.email = email
                user.save()
                login(request, user)
        elif form_type == "phone":
            phone = request.POST.get("phone")
            if not phone:
                return HttpResponseRedirect(reverse('auta:user_profile') + '?error_message=Neplatné údaje.')
            else:
                user.phone = phone
                user.save()
        elif form_type == "password":
            current_password = request.POST.get("current_password")
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")
            user_auth = authenticate(request, email=user.email, password=current_password)
            if user_auth is not None:
                if not password1 or not password2:
                    return HttpResponseRedirect(reverse('auta:user_profile') + '?error_message=Neplatné údaje.')
                if password1 != password2:
                    return HttpResponseRedirect(reverse('auta:user_profile') + '?error_message=Hesla se neshodují.')
                else:
                    user.set_password(password1)
                    user.save()
                    login(request, user)
            else:
                return HttpResponseRedirect(reverse('auta:user_profile') + '?error_message=Neplatné údaje.')
        return HttpResponseRedirect(reverse('auta:user_profile') + '?error_message=Úspěšně upraveno.')
    else:
        return render(request, 'auta/user_profile.html', {'user': user})
    
@login_required
def auto_reserve_view(request, auto_id):
    if request.method == 'POST':
        date = request.POST.get('date-select')
        time = request.POST.get('time-slot-select')
        if not auto_id or not date or not time:
            return HttpResponseRedirect(reverse('auta:homepage') + '?error_message=Neplatné údaje.')
        else:
            auto = Auto.objects.get(pk=auto_id)
            date_time_naive = datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M')
            date_time = timezone.make_aware(date_time_naive)

            if timezone.now() + timedelta(minutes=15) <= date_time <= timezone.now() + timedelta(days=7):
                reservation = Rezervace.objects.create(auto=auto, datum_a_cas=date_time, user=request.user)
                reservation.save()
            else:
                return HttpResponseRedirect(reverse('auta:homepage') + '?error_message=Neplatné údaje.')
            return HttpResponseRedirect(reverse('auta:homepage') + '?error_message=Úspěšně rezervováno.')
        

    else:
        return HttpResponseRedirect(reverse('auta:homepage') + '?error_message=Aj, Chyba!')
    
def get_time_slots(date, auto):
    time_slots = []
    start_time = time(9, 0)
    end_time = time(17, 0)

    while start_time <= end_time:
        current_datetime = timezone.make_aware(datetime.combine(date, start_time))
        if current_datetime > timezone.now() + timedelta(minutes=15):
            time_slots.append(current_datetime)
        start_time = (datetime.combine(date.min, start_time) + timedelta(minutes=30)).time()

    existing_reservations = Rezervace.objects.filter(auto=auto, datum_a_cas__date__range=[date.today(), date.today() + timedelta(days=7)])

    for reservation in existing_reservations:
        time_slots = [slot for slot in time_slots if abs((slot - reservation.datum_a_cas).total_seconds()) >= 30 * 60]
    time_slots = [slot.strftime('%H:%M') for slot in time_slots]
    return time_slots

def get_dates(auto):
    dates = []
    for i in range(7):
        potential_date = date.today() + timedelta(days=i)
        if potential_date.weekday() < 5:
            time_slots = get_time_slots(potential_date, auto)
            if time_slots:
                dates.append(potential_date)
    return dates

def get_time_slots_json(request):
    date_str = request.GET.get('date')
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    auto_id = request.GET.get('auto_id')
    auto = Auto.objects.get(pk=auto_id)
    return JsonResponse({'time_slots': get_time_slots(date, auto)})

def get_dates_json(request):
    auto_id = request.GET.get('auto_id')
    auto = Auto.objects.get(pk=auto_id)
    return JsonResponse({'dates': get_dates(auto)})