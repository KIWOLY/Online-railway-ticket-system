from django.contrib import admin
from .models import Train, Booking

# Register the Train model with Django admin
@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    list_display = ('name', 'source', 'destination', 'departure_time', 'arrival_time', 'seats_available')
    search_fields = ('name', 'source', 'destination')
    list_filter = ('source', 'destination')
    ordering = ('departure_time',)

# Register the Booking model with Django admin
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'train', 'seats_booked', 'booking_date')
    search_fields = ('user__username', 'train__name')
    list_filter = ('train', 'booking_date')
    ordering = ('-booking_date',)
