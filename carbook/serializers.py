# from rest_framework import serializers
# from decimal import Decimal
# from .models import Booking, Car, CarImage, CarMake, CarModel







from rest_framework import serializers
from decimal import Decimal
from .models import Booking, Car, CarImage, CarMake, CarModel

from rest_framework import serializers
from .models import Car, CarModel, CarMake, CarImage

class CarMakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarMake
        fields = ('id', 'name')

class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ('id', 'name', 'make')

class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ('id', 'image')

class CarSerializer(serializers.ModelSerializer):
    model = CarModelSerializer()
    image = CarImageSerializer(many=True)  # Use a nested serializer for CarImage

    class Meta:
        model = Car
        fields = ('id', 'model', 'year', 'available', 'price_per_day', 'image')

    def create(self, validated_data):
        model_data = validated_data.pop('model')
        image_data = validated_data.pop('image')  # Get the image data
        car_make, created = CarMake.objects.get_or_create(name=model_data['make']['name'])
        car_model, created = CarModel.objects.get_or_create(make=car_make, name=model_data['name'])
        car = Car.objects.create(model=car_model, **validated_data)
        
        # Create CarImage objects for the car
        for image in image_data:
            CarImage.objects.create(car=car, **image)
        
        return car


# class CarMakeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CarMake
#         fields = '__all__'

# class CarImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CarImage
#         fields = '__all__'

# class CarModelSerializer(serializers.ModelSerializer):
#     carmake = CarMakeSerializer()

#     class Meta:
#         model = CarModel
#         fields = ('carmake', 'name')

# class CarSerializer(serializers.ModelSerializer):
#     image = CarImageSerializer(many=True, required=False, allow_null=True)

#     class Meta:
#         model = Car
#         fields = ['model', 'year', 'available', 'price_per_day', 'image']

#     def create(self, validated_data):
#         model_data = validated_data.pop('model', None)
#         images_data = validated_data.pop('image', [])

#         if model_data and 'carmake' in model_data:
#             carmake_data = model_data.pop('carmake')
#             carmake, created = CarMake.objects.get_or_create(**carmake_data)
#             carmodel, created = CarModel.objects.get_or_create(make=carmake, **model_data)
#             validated_data['model'] = carmodel

#         car = Car.objects.create(**validated_data)

#         for carimage_data in images_data:
#             carimage, created = CarImage.objects.get_or_create(**carimage_data)
#             car.image.add(carimage)  # Assuming 'image' is a ManyToManyField

#         return car

class CarBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('id', 'user', 'car', 'start_date', 'end_date', 'pickup_time', 'dropoff_time', 'age', 'is_approved', 'total_amount')

    def create(self, validated_data):
        car = validated_data['car']
        start_date = validated_data['start_date']
        end_date = validated_data['end_date']

        # Calculate the day difference between start_date and end_date
        day_difference = (end_date - start_date).days

        # Get the price from the car associated with the booking
        car_price = car.price_per_day

        # Calculate the total_amount based on the price and day difference
        total_amount = car_price * day_difference

        # Update the validated_data with the calculated total_amount
        validated_data['total_amount'] = total_amount

        booking = Booking.objects.create(**validated_data)

        return booking



# class CarBookingSerializer(serializers.ModelSerializer):
#     car = CarSerializer()

#     class Meta:
#         model = Booking
#         fields = ('car', 'start_date', 'end_date', 'pickup_time', 'dropoff_time', 'age', 'is_approved', 'total_amount')

#     def create(self, validated_data):
#         car_data = validated_data.pop('car')
#         duration = (validated_data['end_date'] - validated_data['start_date']).days
#         price_per_day = Decimal(car_data['price_per_day'])
#         total_amount = price_per_day * Decimal(duration)

#         validated_data['total_amount'] = total_amount

#         booking_instance = Booking.objects.create(**validated_data)
#         return booking_instance

#     def update(self, instance, validated_data):
#         car_data = validated_data.get('car', instance.car)
#         instance.start_date = validated_data.get('start_date', instance.start_date)
#         instance.end_date = validated_data.get('end_date', instance.end_date)
#         instance.pickup_time = validated_data.get('pickup_time', instance.pickup_time)
#         instance.dropoff_time = validated_data.get('dropoff_time', instance.dropoff_time)
#         instance.age = validated_data.get('age', instance.age)
#         instance.is_approved = validated_data.get('is_approved', instance.is_approved)

#         duration = (instance.end_date - instance.start_date).days
#         price_per_day = Decimal(car_data['price_per_day'])
#         total_amount = price_per_day * Decimal(duration)
#         instance.total_amount = total_amount

#         instance.save()
#         return instance