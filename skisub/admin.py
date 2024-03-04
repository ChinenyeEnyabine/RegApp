# from django.contrib import admin
from carbook import models
from skisub.models import BillOperation
from django.db.models.signals import post_save
from django.dispatch import receiver
from carbook.models import Car, Booking
from django.contrib import admin
# from skisub.models import BillOperation
from carbook.models import CarMake, Car, CarImage, Booking, CarModel
from hotelbooking.models import Amenity, HotelImage, Hotel
from hotelbooking.models import Booking as hotelbooking
from account.models import Transaction

admin.site.register(BillOperation)

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

class HotelImageInline(admin.TabularInline):
    model = Hotel.images.through  # Through model for the ManyToMany relationship
    extra = 1

class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class HotelAdmin(admin.ModelAdmin):
    inlines = [HotelImageInline]  # Include HotelImage inlines for easy image management
    list_display = ('name', 'price_per_day', 'available', 'location')
    list_filter = ('amenities', 'available')
    search_fields = ('name', 'location')
    list_editable = ('available', 'price_per_day')

class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'hotel', 'check_in_date', 'check_out_date', 'total_amount')
    list_filter = ('user', 'hotel')
    search_fields = ('user__username', 'hotel__name')
    def save_model(self, request, obj, form, change):
        # Calculate the total_amount based on the price of the car and the difference in days
        price_per_day = obj.hotel.price_per_day
        days_difference = (obj.check_out_date - obj.check_in_date).days
        total_amount = price_per_day * days_difference
        obj.total_amount = total_amount
        super().save_model(request, obj, form, change)

# Register your custom admin classes with the Django admin site
admin.site.register(Amenity, AmenityAdmin)
admin.site.register(Hotel, HotelAdmin)
admin.site.register(HotelImage)
admin.site.register(hotelbooking, BookingAdmin)
admin.site.register(Transaction)
# admin.site.register(Transaction)






