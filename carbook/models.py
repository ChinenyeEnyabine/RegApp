from datetime import date
from django.db import models
from datetime import time
from account.models import User

class CarMake(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class CarModel(models.Model):
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name='models')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class CarImage(models.Model):
   
    image = models.ImageField(upload_to='car_images/')
    

class Car(models.Model):
    
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name='cars')
    year = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image = models.ManyToManyField(CarImage, related_name='cars_images')  # Specify a unique related_name here
    
    def __str__(self):
        return f'{self.model.make.name} --- {self.model.name}'

class Booking(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(default=date.today)
    pickup_time = models.TimeField(default=time(8, 0))  # Set default pickup time to 8:00 AM
    dropoff_time = models.TimeField(default=time(17, 0))  # Set default dropoff time to 5:00 PM
    age = models.IntegerField(default=18) 
    is_approved = models.BooleanField(default=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'Booking for {self.car.model.make.name} --- {self.car.model.name}'
