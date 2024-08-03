

from rest_framework import serializers
from decimal import Decimal
from account.models import Transaction, User
from .models import Booking, Car, CarImage, CarMake, CarModel, Order

class CarMakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarMake
        fields = ('id', 'name')

class CarModelSerializer(serializers.ModelSerializer):
    make = CarMakeSerializer()  # Nested serializer to display the car make details

    class Meta:
        model = CarModel
        fields = ('id', 'name', 'make')

class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ('id', 'image')

class CarSerializer(serializers.ModelSerializer):
    model = CarModelSerializer()
    image = CarImageSerializer(many=True)

    class Meta:
        model = Car
        fields = (
            'id', 
            'model', 
            'year', 
            'available', 
            'price_per_day', 
            'image',
            'number_of_passengers', 
            'number_of_doors', 
            'air_conditioning', 
            'transmission', 
            'fuel_type', 
            'max_power_hp', 
            'top_speed_mph'
        )

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

# class CarBookingSerializer(serializers.ModelSerializer):
#     car = CarSerializer()  # Nested serializer to display car details

#     class Meta:
#         model = Booking
#         fields = (
#             'id', 
#             'user', 
#             'car', 
#             'start_date', 
#             'end_date', 
#             'pickup_time', 
#             'dropoff_time', 
#             'age', 
#             'is_approved', 
#             'total_amount', 
#             'pickup_location', 
#             'dropoff_location'
#         )

#     def create(self, validated_data):
#         # user = validated_data['user']
#         car = validated_data['car']
#         start_date = validated_data['start_date']
#         end_date = validated_data['end_date']

#         # Calculate the day difference between start_date and end_date
#         day_difference = (end_date - start_date).days

#         # Get the price from the car associated with the booking
#         car_price = car.price_per_day

#         # Calculate the total_amount based on the price and day difference
#         total_amount = car_price * day_difference
        
#         validated_data['total_amount']=total_amount
#         booking = Booking.objects.create(**validated_data)
#         return booking
        

# class OrderSerializer(serializers.ModelSerializer):
#     booking = CarBookingSerializer()  # Nested serializer to display booking details

#     class Meta:
#         model = Order
#         fields = ('id', 'user', 'booking', 'order_date', 'status', 'total_amount')
#         read_only_fields = ('total_amount',)
#         ref_name = 'CarBookOrder'

#     def create(self, validated_data):
#         accountno = user.account_number
#         user = validated_data['user']
#         booking = validated_data['booking']
#         total_amount = booking.total_amount  # Derive total amount from the booking
        
#         # Check if user has a wallet
#         try:
#             wallet = Transaction.objects.get(accountNumber=accountno)
#         except Transaction.DoesNotExist:
#             raise serializers.ValidationError("Wallet not found for this user.")

#         # Check if the wallet balance is sufficient
#         if wallet.settledAmount >= total_amount:
#             validated_data['total_amount'] = total_amount

#             # Deduct the total_amount from the user's wallet
#             wallet.settledAmount -= total_amount
#             wallet.save()
#             order = Order.objects.create(user=user, booking=booking, total_amount=total_amount, status='pending')
#         else:
#             raise serializers.ValidationError("Insufficient funds in the wallet.")
#         return order
class CarBookingSerializer(serializers.ModelSerializer):
    car = CarSerializer()  # Nested serializer to display car details

    class Meta:
        model = Booking
        fields = (
            'id', 
            'user', 
            'car', 
            'start_date', 
            'end_date', 
            'pickup_time', 
            'dropoff_time', 
            'age', 
            'is_approved', 
            'total_amount', 
            'pickup_location', 
            'dropoff_location'
        )
        read_only_fields = ('total_amount', 'is_approved')

    def validate(self, data):
        # Validate that the end date is after the start date
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if end_date < start_date:
            raise serializers.ValidationError("End date must be after start date.")

        return data

    def create(self, validated_data):
        # Calculate the day difference between start_date and end_date
        car = validated_data['car']
        start_date = validated_data['start_date']
        end_date = validated_data['end_date']
        day_difference = (end_date - start_date).days

        # Get the price from the car associated with the booking
        car_price = car.price_per_day

        # Calculate the total_amount based on the price and day difference
        total_amount = car_price * day_difference

        # Assign calculated total amount and create booking
        validated_data['total_amount'] = total_amount

        booking = Booking.objects.create(**validated_data)
        return booking
    
class OrderSerializer(serializers.ModelSerializer):
    booking = CarBookingSerializer()  # Nested serializer to display booking details
    
    class Meta:
        model = Order
        fields = ('id', 'user', 'booking', 'order_date', 'status', 'total_amount')
        read_only_fields = ('total_amount', 'order_date', 'status')
        ref_name = 'CarBookingOrder'
    def validate(self, data):
        # Validate booking and ensure funds are available
        booking_data = data.get('booking')
        user = self.context['request'].user
        accountno = user.account_number

        # Fetch booking instance
        try:
            booking = Booking.objects.get(id=booking_data['id'])
        except Booking.DoesNotExist:
            raise serializers.ValidationError("Booking not found.")

        # Fetch transaction wallet
        try:
            wallet = Transaction.objects.get(accountNumber=accountno)
        except Transaction.DoesNotExist:
            raise serializers.ValidationError("Wallet not found for this user.")

        # Check wallet balance
        if wallet.settledAmount < booking.total_amount:
            raise serializers.ValidationError("Insufficient funds in the wallet.")

        return data

    def create(self, validated_data):
        user = validated_data['user']
        booking_data = validated_data['booking']
        booking = Booking.objects.get(id=booking_data['id'])

        # Check if user has a wallet
        accountno = user.account_number
        wallet = Transaction.objects.get(accountNumber=accountno)

        # Deduct the total_amount from the user's wallet
        wallet.settledAmount -= booking.total_amount
        wallet.save()

        # Create order with derived total amount
        order = Order.objects.create(
            user=user,
            booking=booking,
            total_amount=booking.total_amount,
            status='confirmed'
        )

        # Mark booking as approved
        booking.is_approved = True
        booking.save()

        return order
