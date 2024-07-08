from django.db import models
from django.db import models
from account.models import User
class Amenity(models.Model):
    name = models.CharField(max_length=50)
    # hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
class HotelImage(models.Model):
    # hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='hotel_images/')

    # def __str__(self):
    #     return f"Image for {self.hotel.name}"
class Hotel(models.Model):
    name = models.CharField(max_length=255)
    # image = models.ImageField(upload_to='hotels/')  # You may need to configure MEDIA_ROOT and MEDIA_URL in settings.py
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    description = models.TextField()
    location=models.CharField(max_length=255)
    amenities = models.ManyToManyField(Amenity, blank=True,related_name='hotels') 
    images = models.ManyToManyField(HotelImage, blank=True, related_name='hotels')

    def __str__(self):
        return self.name

# Model to represent hotel bookings
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='bookin')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.hotel.name
class HotelOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')])
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"
