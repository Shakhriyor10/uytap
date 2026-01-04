from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("api/listings/", views.listings_data, name="listings_data"),
    path("api/listings/<int:listing_id>/", views.listing_detail, name="listing_detail"),
]