from django.http import JsonResponse
from django.shortcuts import render
from django.templatetags.static import static
from django.utils.dateparse import parse_date

from .models import Availability, Listing


def home(request):
    listings = Listing.objects.filter(is_active=True)

    city = request.GET.get("city")
    property_type = request.GET.get("property_type")
    check_in = request.GET.get("check_in")
    check_out = request.GET.get("check_out")

    if city:
        listings = listings.filter(city__icontains=city)
    if property_type:
        listings = listings.filter(property_type=property_type)

    property_types = Listing.PROPERTY_TYPES
    cities = Listing.objects.values_list("city", flat=True).distinct()

    context = {
        "listings": listings,
        "property_types": property_types,
        "cities": cities,
        "selected_city": city,
        "selected_type": property_type,
        "selected_check_in": check_in,
        "selected_check_out": check_out,
    }
    return render(request, "home.html", context)


def _apply_filters(queryset, city=None, property_type=None, check_in=None, check_out=None, bounds=None):
    if city:
        queryset = queryset.filter(city__icontains=city)
    if property_type:
        queryset = queryset.filter(property_type=property_type)

    if bounds:
        try:
            south, west, north, east = bounds
            queryset = queryset.filter(
                latitude__isnull=False,
                longitude__isnull=False,
                latitude__gte=south,
                latitude__lte=north,
                longitude__gte=west,
                longitude__lte=east,
            )
        except (TypeError, ValueError):
            pass

    if check_in and check_out and check_out > check_in:
        unavailable = Availability.objects.filter(
            date__gte=check_in, date__lt=check_out, is_available=False
        ).values_list("listing_id", flat=True)
        queryset = queryset.exclude(id__in=unavailable)

    return queryset


def listings_data(request):
    listings = Listing.objects.filter(is_active=True)

    city = request.GET.get("city")
    property_type = request.GET.get("property_type")
    check_in = parse_date(request.GET.get("check_in") or "")
    check_out = parse_date(request.GET.get("check_out") or "")

    bounds = None
    south = request.GET.get("south")
    west = request.GET.get("west")
    north = request.GET.get("north")
    east = request.GET.get("east")

    if all([south, west, north, east]):
        try:
            bounds = (float(south), float(west), float(north), float(east))
        except ValueError:
            bounds = None

    listings = _apply_filters(
        listings,
        city=city,
        property_type=property_type,
        check_in=check_in,
        check_out=check_out,
        bounds=bounds,
    )

    results = []
    for listing in listings:
        main_image = listing.get_main_image()
        image_url = (
            request.build_absolute_uri(main_image.image.url)
            if main_image
            else request.build_absolute_uri(static("placeholder.png"))
        )
        results.append(
            {
                "id": listing.id,
                "title": listing.title,
                "city": listing.city,
                "address": listing.address,
                "price": float(listing.price_per_day),
                "lat": float(listing.latitude) if listing.latitude is not None else None,
                "lng": float(listing.longitude) if listing.longitude is not None else None,
                "property_type": listing.get_property_type_display(),
                "image": image_url,
            }
        )

    return JsonResponse({"results": results})