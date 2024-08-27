from datetime import time
from django.db import models
from django.forms import ValidationError
from account.models import User

class Amenity(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class HotelImage(models.Model):
    image = models.ImageField(upload_to='hotel_images/')

class Hotel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    amenities = models.ManyToManyField(Amenity, blank=True, related_name='hotels')
    images = models.ManyToManyField(HotelImage, blank=True, related_name='hotels')

    def __str__(self):
        return self.name


class RoomType(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='room_types')
    name = models.CharField(max_length=255)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} at {self.hotel.name}"

    def is_available(self):
        return self.available

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='bookings')
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    check_in_time = models.TimeField(default=time(0, 0))  # 12:00 AM
    check_out_time = models.TimeField(default=time(23, 59))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    guest=models.IntegerField(default=1)

    def __str__(self):
        return f"Booking at {self.room_type.hotel.name} - {self.room_type.name}"

    def clean(self):
        # Ensure check-in date is before check-out date
        if self.check_in_date >= self.check_out_date:
            raise ValidationError("Check-out date must be after check-in date.")

        # Check if the room type is available
        if not self.room_type.is_available():
            raise ValidationError("The selected room type is not available.")

        super().clean()

class HotelOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('confirmed', 'Confirmed'),
            ('cancelled', 'Cancelled')
        ],
        default='confirmed'  # Default status to 'pending'
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"
