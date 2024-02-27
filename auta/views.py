from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from datetime import time, timedelta, date
from django.utils import timezone
from django.contrib import messages
import requests

from .models import Auto, Rezervace, CustomUser, Image
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

    context = {
        'auta_list': auta_list,
        'show_popup': show_popup,
        'email': email,
        'error_message': error_message,
        'register': register,
        'login': login,
    }

    return render(request, 'auta/homepage.html', context)

def contact_view(request):
    return render(request, 'auta/contact.html')

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
        elif len(password1.strip()) < 6:
            messages.error(request, 'Heslo musí mít alespoň 6 znaků.')
            return HttpResponseRedirect(reverse('auta:homepage') + '?show_popup=True&register=True')
        elif len(phone.strip()) < 9 or len(phone.strip()) > 13:
            messages.error(request, 'Neplatné telefonní číslo.')
            return HttpResponseRedirect(reverse('auta:homepage') + '?show_popup=True&register=True')
        elif len(full_name.strip()) < 3 or len(full_name.strip()) > 50:
            messages.error(request, 'Neplatné jméno.')
            return HttpResponseRedirect(reverse('auta:homepage') + '?show_popup=True&register=True')
        elif len(email.strip()) < 5 or len(email.strip()) > 50:
            messages.error(request, 'Neplatný email.')
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
                messages.error(request, 'Neplatné údaje.')
                return HttpResponseRedirect(reverse('auta:user_profile'))
            elif len(full_name.strip()) < 3 or len(full_name.strip()) > 50:
                messages.error(request, 'Neplatné jméno.')
                return HttpResponseRedirect(reverse('auta:user_profile'))
            else:
                user.full_name = full_name
                user.save()
        elif form_type == "email":
            email = request.POST.get("email")
            if not email:
                messages.error(request, 'Neplatné údaje.')
                return HttpResponseRedirect(reverse('auta:user_profile'))
            elif len(email.strip()) < 5 or len(email.strip()) > 50:
                messages.error(request, 'Neplatný email.')
                return HttpResponseRedirect(reverse('auta:user_profile'))
            else:
                user.email = email
                user.save()
                login(request, user)
        elif form_type == "phone":
            phone = request.POST.get("phone")
            if not phone:
                messages.error(request, 'Neplatné údaje.')
                return HttpResponseRedirect(reverse('auta:user_profile'))
            elif len(phone.strip()) < 9 or len(phone.strip()) > 13:
                messages.error(request, 'Neplatné telefonní číslo.')
                return HttpResponseRedirect(reverse('auta:user_profile'))
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
                    messages.error(request, 'Neplatné údaje.')
                    return HttpResponseRedirect(reverse('auta:user_profile'))
                elif password1 != password2:
                    messages.error(request, 'Hesla se neshodují.')
                    return HttpResponseRedirect(reverse('auta:user_profile'))
                elif len(password1.strip()) < 6:
                    messages.error(request, 'Heslo musí mít alespoň 6 znaků.')
                    return HttpResponseRedirect(reverse('auta:user_profile'))
                else:
                    user.set_password(password1)
                    user.save()
                    login(request, user)
            else:
                messages.error(request, 'Neplatné údaje.')
                return HttpResponseRedirect(reverse('auta:user_profile'))
        messages.success(request, 'Úspěšně upraveno.')
        return HttpResponseRedirect(reverse('auta:user_profile'))
    else:
        return render(request, 'auta/user_profile.html', {'user': user})
    
@login_required
def auto_reserve_view(request, auto_id):
    if request.method == 'POST':
        date = request.POST.get('date-select')
        time = request.POST.get('time-slot-select')
        if not auto_id or not date or not time:
            messages.error(request, 'Neplatné údaje.')
            return HttpResponseRedirect(reverse('auta:homepage'))
        else:
            auto = Auto.objects.get(pk=auto_id)
            date_time_naive = datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M')
            date_time = timezone.make_aware(date_time_naive)

            if timezone.now() + timedelta(minutes=15) <= date_time <= timezone.now() + timedelta(days=7):
                reservation = Rezervace.objects.create(auto=auto, datum_a_cas=date_time, user=request.user)
                reservation.save()
            else:
                messages.error(request, 'Neplatné údaje.')
                return HttpResponseRedirect(reverse('auta:homepage'))
            messages.success(request, 'Úspěšně rezervováno. Vaše rezervace najdete ve vašem profilu.')
            return HttpResponseRedirect(reverse('auta:detail', args=(auto_id,)))
    else:
        messages.error(request, 'Nepodařilo se rezervovat.')
        return HttpResponseRedirect(reverse('auta:homepage'))
    
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

@login_required
def reservation_delete_view(request, reservation_id):
    try:
        reservation = get_object_or_404(Rezervace, id=reservation_id)
        if reservation.user == request.user:
            reservation.delete()
            messages.success(request, 'Rezervace úspěšně smazána.')
            return HttpResponseRedirect(reverse('auta:user_profile'))
        else:
            messages.error(request, 'Nepodařilo se smazat rezervaci.')
            return HttpResponseRedirect(reverse('auta:user_profile'))
    except Rezervace.DoesNotExist:
        messages.error(request, 'Rezervace neexistuje.')
        return HttpResponseRedirect(reverse('auta:user_profile'))

@login_required
def auto_edit_view(request, auto_id):
    if not request.user.is_staff:
        messages.error(request, 'Auta můžou upravovat pouze zaměstnanci.')
        return HttpResponseRedirect(reverse('auta:homepage'))
    
    auto = Auto.objects.get(pk=auto_id)
    if request.method == 'POST':
        fields = ['znacka', 'model', 'rok_vyroby', 'cena', 'stav_tachometru', 'palivo', 'barva', 'prevodovka', 'popis']
        upraveno = False
        for field in fields:
            value = request.POST.get(field)
            print(field, value, getattr(auto, field))
            if not value:
                messages.error(request, 'Neplatné údaje - ' + field)
                return HttpResponseRedirect(reverse('auta:auto_edit', args=[auto_id]))
            elif field == 'rok_vyroby' or field == 'cena' or field == 'stav_tachometru':
                try:
                    value = int(value)
                    setattr(auto, field, value)
                except ValueError:
                    messages.error(request, 'Neplatné údaje - ' + field)
            elif getattr(auto, field) != type(getattr(auto, field))(value):
                upraveno = True
                setattr(auto, field, value)
                auto.save()
            else:
                pass
        #Existing images
        images = Image.objects.filter(auto_id=auto.id).order_by('order')
        for image in images:
            try:
                edit_image = request.POST.get('image' + str(image.id))
                if edit_image == '' or edit_image == None:
                    image.delete()
                    upraveno = True
                elif edit_image != image.url:
                    response = requests.get(edit_image)
                    if response.status_code != 200:
                        raise ValueError('Neplatná adresa obrázku')
                    content_type = response.headers['content-type']
                    if not content_type.startswith('image/'):
                        raise ValueError('Adresa neobsahuje obrázek')
                    image.url = edit_image
                    upraveno = True
                    image.save()
                else:
                    pass
            except (requests.ConnectionError, ValueError):
                messages.error(request, 'Neplatný obrázek')

        #New image
        new_image = request.POST.get('image')
        if not new_image:
            pass
        else:
            try:
                new_image = new_image.strip()
                response = requests.get(new_image)
                if response.status_code != 200:
                    raise ValueError('Neplatná adresa obrázku')
                content_type = response.headers['content-type']
                if not content_type.startswith('image/'):
                    raise ValueError('Adresa neobsahuje obrázek')
                order = Image.objects.filter(auto_id=auto.id).count() + 1
                img_obj = Image.objects.create(auto_id=auto, url=new_image, order=order)
                img_obj.save()
                upraveno = True
            except (requests.ConnectionError, ValueError):
                messages.error(request, 'Neplatný obrázek')
        auto.save()
        if upraveno:
            messages.success(request, 'Úspěšně upraveno.')
        return HttpResponseRedirect(reverse('auta:detail', args=[auto_id]))
    else:
        auto.images = Image.objects.filter(auto_id=auto.id).order_by('order')
        context = {
            'auto': auto,
            'auto.images': auto.images,
        }
        return render(request, 'auta/edit_car.html', context)
    
@login_required
def auto_delete_view(request, auto_id):
    if not request.user.is_staff:
        messages.error(request, 'Auta můžou mazat pouze zaměstnanci.')
        return HttpResponseRedirect(reverse('auta:homepage'))
    auto = get_object_or_404(Auto, id=auto_id)
    auto.delete()
    messages.success(request, 'Auto bylo úspěšně smazáno.')
    return HttpResponseRedirect('/')

@login_required
def auto_create_view(request):
    if not request.user.is_staff:
        messages.error(request, 'Auta můžou vytvářet pouze zaměstnanci.')
        return HttpResponseRedirect(reverse('auta:homepage'))
    
    if request.method == 'POST':
        fields = ['znacka', 'model', 'rok_vyroby', 'cena', 'stav_tachometru', 'palivo', 'barva', 'prevodovka', 'popis']
        auto = Auto()
        context = {}
        error_counter = 0
        for field in fields:
            value = request.POST.get(field)
            if not value:
                messages.error(request, 'Neplatné údaje - ' + field)
                error_counter += 1
            elif field == 'rok_vyroby' or field == 'cena' or field == 'stav_tachometru':
                try:
                    value = int(value)
                    setattr(auto, field, value)
                    context[field] = value
                except ValueError:
                    error_counter += 1
                    messages.error(request, 'Neplatné údaje - ' + field)
            else:
                setattr(auto, field, value)
                context[field] = value
        image = request.POST.get('image')
        if not image:
            error_counter += 1
            messages.error(request, 'Neplatný obrázek')
        else:
            try:
                image = image.strip()
                response = requests.get(image)
                if response.status_code != 200:
                    raise ValueError('Neplatná adresa obrázku')
                content_type = response.headers['content-type']
                if not content_type.startswith('image/'):
                    raise ValueError('Adresa neobsahuje obrázek')
                order = Image.objects.filter(auto_id=auto.id).count() + 1
                context['image'] = image
            except (requests.ConnectionError, ValueError):
                error_counter += 1
                messages.error(request, 'Neplatný obrázek')
        if error_counter > 0:
            return render(request, 'auta/create_car.html', context)
        else:
            auto.save()
            img_obj = Image.objects.create(auto_id=auto, url=image.strip(), order=order)
            img_obj.save()
            messages.success(request, 'Úspěšně vytvořeno.')
        return HttpResponseRedirect(reverse('auta:detail', args=[auto.id]))
    else:
        return render(request, 'auta/create_car.html')