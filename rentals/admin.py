from django.contrib import admin
from .models import (
    Profile, Listing, ListingImage,
    Availability, Booking, Review,
    Wishlist, Payment
)


# ==========================
# PROFILE
# ==========================
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "is_host", "rating")
    search_fields = ("user__username", "phone")
    list_filter = ("is_host",)


# ==========================
# LISTING IMAGE INLINE
# ==========================
class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1
    fields = ("image", "caption", "is_cover")


# ==========================
# AVAILABILITY INLINE
# ==========================
class AvailabilityInline(admin.TabularInline):
    model = Availability
    extra = 0
    fields = ("date", "is_available")
    ordering = ("date",)


# ==========================
# LISTING
# ==========================
@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = (
        "title", "city", "price_per_day", "host", "property_type", "is_active"
    )
    list_filter = ("city", "property_type", "is_active")
    search_fields = ("title", "city__name", "host__username")
    inlines = [ListingImageInline, AvailabilityInline]
    readonly_fields = ("created_at", "updated_at")


# ==========================
# BOOKING
# ==========================
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "id", "listing", "guest", "check_in", "check_out", "total_price", "status"
    )
    list_filter = ("status", "check_in", "check_out")
    search_fields = ("listing__title", "guest__username")
    readonly_fields = ("created_at", "updated_at")


# ==========================
# REVIEW
# ==========================
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("listing", "guest", "rating", "created_at")
    list_filter = ("rating",)
    search_fields = ("listing__title", "guest__username")


# ==========================
# WISHLIST
# ==========================
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("user", "listing", "created_at")
    search_fields = ("user__username", "listing__title")


# ==========================
# PAYMENT
# ==========================
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "booking", "amount", "method", "status", "created_at")
    list_filter = ("status", "method")
    search_fields = ("booking__id",)
    readonly_fields = ("created_at",)
