from rest_framework import serializers
from account.models import Transaction
from hotelbooking.models import Amenity, Booking, Hotel, HotelImage, HotelOrder, RoomType

class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = "__all__"

class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = "__all__"

class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = "__all__"

class HotelSerializer(serializers.ModelSerializer):
    amenities = AmenitySerializer(many=True)
    images = HotelImageSerializer(many=True)
    room_types = RoomTypeSerializer(many=True)

    class Meta:
        model = Hotel
        fields = ['id', 'name', 'description', 'location', 'amenities', 'images', 'room_types']

    def create(self, validated_data):
        amenities_data = validated_data.pop('amenities', [])
        images_data = validated_data.pop('images', [])
        room_types_data = validated_data.pop('room_types', [])

        hotel = Hotel.objects.create(**validated_data)

        for amenity in amenities_data:
            amenity_obj, created = Amenity.objects.get_or_create(**amenity)
            hotel.amenities.add(amenity_obj)

        for image in images_data:
            image_obj, created = HotelImage.objects.get_or_create(**image)
            hotel.images.add(image_obj)

        for room_type in room_types_data:
            RoomType.objects.create(hotel=hotel, **room_type)

        return hotel

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'room_type', 'check_in_date', 'check_out_date', 'total_amount']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['room_type'] = RoomTypeSerializer(instance.room_type).data
        return representation

    def create(self, validated_data):
        user = validated_data['user']
        accountno = user.account_number
        room_type = validated_data['room_type']
        check_in_date = validated_data['check_in_date']
        check_out_date = validated_data['check_out_date']

        delta = check_out_date - check_in_date
        total_days = delta.days

        total_amount = room_type.price_per_day * total_days

        validated_data['total_amount'] = total_amount

        try:
            wallet = Transaction.objects.get(accountNumber=accountno)
        except Transaction.DoesNotExist:
            raise serializers.ValidationError("Wallet not found for this user.")

        if wallet.settledAmount >= total_amount:
            wallet.settledAmount -= total_amount
            wallet.save()

            booking = Booking.objects.create(**validated_data)
            return booking
        else:
            raise serializers.ValidationError("Insufficient funds in the wallet.")
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelOrder
        fields = ('id', 'user', 'booking', 'order_date', 'status', 'total_amount')
        read_only_fields = ('total_amount',)

    def create(self, validated_data):
        user = validated_data['user']
        booking = validated_data['booking']
        total_amount = booking.total_amount  # Derive total amount from the booking

        order = HotelOrder.objects.create(user=user, booking=booking, total_amount=total_amount, status='pending')
        return order