from django.urls import path, re_path
from django.views.generic import RedirectView

from . import views

app_name = "auta"
urlpatterns = [
    path("", views.homepage_view, name="homepage"),
    path("auto/<int:auto_id>/", views.detail_view, name="detail"),
    path("login/", views.user_login, name="user_login"),
    path("logout/", views.user_logout, name="user_logout"),
    path("register/", views.user_register, name="user_register"),
    path("profile/", views.user_profile, name="user_profile"),
    path("profile/edit/", views.user_profile_edit, name="user_profile_edit"),
    #re_path(r'^.*$', RedirectView.as_view(url='/', permanent=True), name='index'),
]