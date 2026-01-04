from django.shortcuts import render
from .models import Listing, ListingImage

def home(request):
    listings = Listing.objects.filter(is_active=True)

    # Фильтры
    city = request.GET.get("city")
    property_type = request.GET.get("property_type")

    if city:
        listings = listings.filter(city__icontains=city)
    if property_type:
        listings = listings.filter(property_type=property_type)

    property_types = Listing.PROPERTY_TYPES
    cities = Listing.objects.values_list('city', flat=True).distinct()

    context = {
        "listings": listings,
        "property_types": property_types,
        "cities": cities,
        "selected_city": city,
        "selected_type": property_type,
    }
    return render(request, "home.html", context)