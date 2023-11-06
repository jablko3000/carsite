from django.urls import path

from . import views

app_name = "auta"
urlpatterns = [
    path("", views.HomePageView.as_view(), name="index"),
]