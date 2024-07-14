# from django.contrib import admin
# from carbook import models
# from skisub.models import BillOperation, UtilityOrder
from django.db.models.signals import post_save
from django.dispatch import receiver
from carbook.models import Car, Booking, Order
from django.contrib import admin
# from skisub.models import BillOperation
from carbook.models import CarMake, Car, CarImage, Booking, CarModel
from hotelbooking.models import Amenity, HotelImage, Hotel, HotelOrder,RoomType
from hotelbooking.models import Booking as hotelbooking
from account.models import Transaction

# admin.site.register(BillOperation)

from django.db.models.signals import post_save
from django.dispatch import receiver

class CarImageInline(admin.TabularInline):
    model = Car.image.through  # Through model for the ManyToMany relationship
    extra = 1

class CarAdmin(admin.ModelAdmin):
    inlines = [CarImageInline]  # Include CarImage inlines for easy image management
    list_display = ('model', 'year', 'available', 'price_per_day')
    list_filter = ('model__make', 'available')
    search_fields = ('model__name', 'year')
    list_editable = ('available', 'price_per_day')

class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'start_date', 'end_date', 'pickup_time', 'dropoff_time', 'is_approved', 'total_amount')
    list_filter = ('user', 'is_approved')
    search_fields = ('user__username', 'car__model__name')
    list_editable = ('is_approved', 'total_amount','car','start_date','end_date', 'pickup_time', 'dropoff_time')
    
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

   

# Register your custom admin classes with the Django admin site
admin.site.register(CarMake)
admin.site.register(CarModel)
admin.site.register(Car, CarAdmin)
admin.site.register(CarImage)
admin.site.register(Booking, BookingAdmin)
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









