from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("api/listings/", views.listings_data, name="listings_data"),
]
