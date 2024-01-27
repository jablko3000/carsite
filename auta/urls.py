from django.urls import path, re_path
from django.views.generic import RedirectView

from . import views

app_name = "auta"
urlpatterns = [
    path("", views.homepage_view, name="homepage"),
    path("auto/<int:auto_id>/", views.detail_view, name="detail"),
    path("auto/<int:auto_id>/edit/", views.auto_edit_view, name="auto_edit"),
    path("auto/<int:auto_id>/reserve/", views.auto_reserve_view, name="auto_reserve"),
    path("login/", views.user_login, name="user_login"),
    path("logout/", views.user_logout, name="user_logout"),
    path("register/", views.user_register, name="user_register"),
    path("profile/", views.user_profile, name="user_profile"),
    path("profile/edit/", views.user_profile_edit, name="user_profile_edit"),
    path('get_time_slots_json', views.get_time_slots_json, name='get_time_slots_json'),
    path('get_dates_json', views.get_dates_json, name='get_dates_json'),
    #re_path(r'^.*$', RedirectView.as_view(url='/', permanent=True), name='index'),
]