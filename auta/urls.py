from django.urls import path

from . import views

app_name = "auta"
urlpatterns = [
    path("", views.HomePageView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:auto_id>/reserve/", views.reserve, name="reserve"),
]