# from django.contrib import admin
# from carbook import models
# from skisub.models import BillOperation, UtilityOrder
from django.db.models.signals import post_save
from django.dispatch import receiver
import account
from carbook.models import Car, Booking, Order
from django.contrib import admin
# from skisub.models import BillOperation
from carbook.models import CarMake, Car, CarImage, Booking, CarModel
from hotelbooking.models import Amenity, HotelImage, Hotel, HotelOrder,RoomType
from hotelbooking.models import Booking as hotelbooking
from account.models import Transaction,AbstractUser

# admin.site.register(BillOperation)

# admin.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import admin
from carbook.models import (
    CarMake,
    CarModel,
    Car,
    CarImage,
    Booking,
    Order,
)

# Inline class for managing Car Images
class CarImageInline(admin.TabularInline):
    model = Car.image.through  # Corrected: Access the 'through' table for the ManyToMany relationship
    extra = 1
    verbose_name = "Car Image"
    verbose_name_plural = "Car Images"

# Custom admin class for Car
class CarAdmin(admin.ModelAdmin):
    inlines = [CarImageInline]  # Include CarImage inlines for easy image management
    list_display = (
        'model',
        'year',
        'available',
        'price_per_day',
        'transmission',
        'fuel_type',
        'number_of_passengers',
        'max_power_hp',
        'top_speed_mph',
        'air_conditioning'
    )
    list_filter = (
        'model__make',
        'available',
        'fuel_type',
        'transmission',
        'air_conditioning'
    )
    search_fields = (
        'model__name',
        'year'
    )
    list_editable = (
        'available',
        'price_per_day',
        'transmission',
        'fuel_type',
        'air_conditioning',
        'number_of_passengers',
        'max_power_hp',
        'top_speed_mph'
    )

    # Add fieldsets for better organization
    fieldsets = (
        (None, {
            'fields': ('model', 'year', 'available', 'price_per_day', 'image'),
        }),
        ('Car Details', {
            'fields': (
                'number_of_passengers',
                'number_of_doors',
                'transmission',
                'fuel_type',
                'air_conditioning',
                'max_power_hp',
                'top_speed_mph'
            ),
            'classes': ('collapse',),
        }),
    )

# Custom admin class for Booking
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'car',
        'start_date',
        'end_date',
        'pickup_time',
        'dropoff_time',
        'is_approved',
        'total_amount',
        'pickup_location',
        'dropoff_location',
    )
    list_filter = (
        'user',
        'is_approved',
        'start_date',
        'end_date'
    )
    search_fields = (
        'user__username',
        'car__model__name',
        'pickup_location',
        'dropoff_location'
    )
    list_editable = (
        'is_approved',
        'total_amount',
        'car',
        'start_date',
        'end_date',
        'pickup_time',
        'dropoff_time',
        'pickup_location',
        'dropoff_location'
    )

    def save_model(self, request, obj, form, change):
        # Calculate the total_amount based on the price of the car and the difference in days
        price_per_day = obj.car.price_per_day
        days_difference = (obj.end_date - obj.start_date).days
        total_amount = price_per_day * days_difference
        obj.total_amount = total_amount
        super().save_model(request, obj, form, change)

    def update_total_amount(self, obj, price_per_day):
        days_difference = (obj.end_date - obj.start_date).days
        total_amount = price_per_day * days_difference
        obj.total_amount = total_amount

    def save_related(self, request, form, formsets, change):
        # This method is called when saving related objects (e.g., Car) of a Booking
        super().save_related(request, form, formsets, change)
        # Check if the car's price_per_day has changed
        if change and 'car' in form.changed_data:
            # Update the total_amount based on the new price_per_day
            self.update_total_amount(form.instance, form.instance.car.price_per_day)
            form.instance.save()

# Custom admin class for Order
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'booking',
        'order_date',
        'status',
        'total_amount'
    )
    list_filter = (
        'status',
        'order_date'
    )
    search_fields = (
        'user__username',
        'booking__car__model__name',
        'status'
    )
    list_editable = (
        'status',
        'total_amount'
    )

    # Optional: Custom actions to manage orders
    actions = ['mark_as_confirmed', 'mark_as_cancelled']

    def mark_as_confirmed(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f"{updated} orders marked as confirmed.")

    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f"{updated} orders marked as cancelled.")

    mark_as_confirmed.short_description = "Mark selected orders as confirmed"
    mark_as_cancelled.short_description = "Mark selected orders as cancelled"

# Register your custom admin classes with the Django admin site
admin.site.register(CarMake)
admin.site.register(CarModel)
admin.site.register(Car, CarAdmin)
admin.site.register(CarImage)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Order, OrderAdmin)

#####################################################################################

# from .models import Amenity, Hotel, HotelImage, RoomType, Booking, HotelOrder

class HotelImageInline(admin.TabularInline):
    model = Hotel.images.through  # Through model for the ManyToMany relationship
    extra = 1

class RoomTypeInline(admin.TabularInline):
    model = RoomType
    extra = 1

class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class HotelAdmin(admin.ModelAdmin):
    inlines = [HotelImageInline, RoomTypeInline]  # Include HotelImage and RoomType inlines for easy management
    list_display = ('name', 'location')
    list_filter = ('amenities', 'room_types__available')
    search_fields = ('name', 'location')

class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'room_type', 'check_in_date', 'check_out_date', 'total_amount')
    list_filter = ('user', 'room_type__hotel')
    search_fields = ('user__username', 'room_type__hotel__name')

    def save_model(self, request, obj, form, change):
        # Calculate the total_amount based on the price of the room type and the difference in days
        price_per_day = obj.room_type.price_per_day
        days_difference = (obj.check_out_date - obj.check_in_date).days
        total_amount = price_per_day * days_difference
        obj.total_amount = total_amount
        super().save_model(request, obj, form, change)

class HotelOrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'booking', 'order_date', 'status', 'total_amount')
    list_filter = ('status',)
    search_fields = ('user__username', 'booking__room_type__hotel__name')

# Register your custom admin classes with the Django admin site
admin.site.register(Amenity, AmenityAdmin)
admin.site.register(Hotel, HotelAdmin)
admin.site.register(HotelImage)
admin.site.register(RoomType)
admin.site.register(hotelbooking, BookingAdmin)
admin.site.register(HotelOrder, HotelOrderAdmin)
# admin.site.register(AbstractUser)
# admin.site.register(UtilityOrder)

################################################################
from django.contrib import admin
from .models import ServiceProvider, AirtimeBundle, DataBundle, Transaction

@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

@admin.register(AirtimeBundle)
class AirtimeBundleAdmin(admin.ModelAdmin):
    list_display = ('service_provider', 'name', 'price')
    search_fields = ('service_provider__name', 'name')

@admin.register(DataBundle)
class DataBundleAdmin(admin.ModelAdmin):
    list_display = ('service_provider', 'name', 'price', 'data_volume', 'validity_period')
    search_fields = ('service_provider__name', 'name', 'data_volume', 'validity_period')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction_type', 'phone_number', 'transaction_date', 'transaction_status', 'transaction_id')
    search_fields = ('user__username', 'phone_number', 'transaction_id')
    list_filter = ('transaction_type', 'transaction_status')









