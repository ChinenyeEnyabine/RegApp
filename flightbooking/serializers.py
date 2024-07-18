from rest_framework import serializers
from rest_framework import generics
from .models import Booking, Flight


# class BookingSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Booking
#         fields = ['id','flight','adults','children','trip_type','departure_date','return_date','total_amount']


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = ['id', 'flight', 'adults', 'children', 'trip_type', 'departure_date', 'return_date', 'total_amount']
        ref_name = 'FlightBooking'
    def create(self, validated_data):
        """
        Create and return a new Booking instance with the validated data.
        """
        # Your custom logic for creating a Booking instance goes here
        # For example:
        booking = Booking.objects.create(**validated_data)
        return booking

    def update(self, instance, validated_data):
        """
        Update and return an existing Booking instance with the validated data.
        """
        # Your custom logic for updating other fields goes here
        instance.adults = validated_data.get('adults', instance.adults)
        instance.children = validated_data.get('children', instance.children)
        instance.trip_type = validated_data.get('trip_type', instance.trip_type)
        instance.departure_date = validated_data.get('departure_date', instance.departure_date)
        instance.return_date = validated_data.get('return_date', instance.return_date)
        
        # Update the flight and let the model's logic calculate total_amount
        flight = validated_data.get('flight', instance.flight)
        if flight and flight.price != instance.flight.price:
            instance.flight = flight  # Update the flight to trigger model's logic
        
        # Save the instance
        instance.save()
        
        return instance


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model=Flight
        fields="__all__"
    # def create(self, validated_data):
    #     flight=Flight.objects.create(
    #     departure_location=self.validated_data['departure_location'],
    #     destination=self.validated_data['destination'],
    #     departure_date=self.validated_data['departure_date'],
    #     returning_date=self.validated_data['returning_date'],
    #     adult_price=self.validated_data['adult_price'],
    #     child_price=self.validated_data['child_price'],
    #     )
    #     return flight
    
class ListBookingSerializer(serializers.ModelSerializer):
    flight=FlightSerializer(read_only=True)
    class Meta:
        model=Booking
        fields = ['id','flight','adults','children','trip_type','departure_date','return_date','total_amount']

    # def Create(self, validated_data):
    #     booking=Booking.objects.create(
    #         flight=self.validated_data.pop('flight'),
    #         adults=self.validated_data['adults'],
    #         children=self.validated_data['children'],
    #         trip_type=self.validated_data['trip_type'],
    #         departure_date=self.validated_data['departure_date'],
    #         returning_date=self.validated_data['returning_date'],
    #         total_amount=self.validated_data['total_amount'],
    #     )
        
       
    #     return booking
        



class AdminFlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'  # Expose all fields, including 'price', to admin
        