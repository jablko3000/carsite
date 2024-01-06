from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views import generic
from django.shortcuts import render, get_object_or_404
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

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
    context = {
        'auto': auto,
        'auto.images': auto.images,
    }
    return render(request, 'auta/detail.html', context)

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('auta:homepage') + '?error_message=Úspěšně přihlášeno.')
        else:
            return HttpResponseRedirect(reverse('auta:homepage') + '?show_popup=True&email=' + email + '&error_message=Neplatné přihlašovací údaje.&login=True')
    else:
        return HttpResponseRedirect(reverse('auta:homepage') + '?error_message=Aj, Chyba!&login=True')
    
@login_required
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect(reverse('auta:homepage') + '?error_message=Úspěšně odhlášeno.')
    else:
        return HttpResponseRedirect(reverse('auta:homepage') + '?error_message=Aj, Chyba!&logout=True')

def user_register(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        if not email or not password1 or not password2 or not full_name or not phone:
            return HttpResponseRedirect(reverse('auta:homepage') + '?show_popup=True&error_message=Neplatné přihlašovací údaje.&register=True')
        if password1 != password2:
            return HttpResponseRedirect(reverse('auta:homepage') + '?show_popup=True&error_message=Neplatné přihlašovací údaje.&register=True')
        else:
            if CustomUser.objects.filter(email=email).exists():
                return HttpResponseRedirect(reverse('auta:homepage') + '?show_popup=True&error_message=Uživatel s tímto emailem již existuje.&register=True')
            else:
                user = CustomUser.objects.create_user(email, password1, phone, full_name)
                user.save()
                login(request, user)
                return HttpResponseRedirect(reverse('auta:homepage') + '?error_message=Úspěšně zaregistrováno.')
    else:
        return HttpResponseRedirect(reverse('auta:homepage') + '?error_message=Aj, Chyba!&register=True')

@login_required
def user_profile(request):
    user = request.user
    return render(request, 'auta/user_profile.html', {'user': user})

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