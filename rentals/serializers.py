from rest_framework import serializers
from .models import Car, Reservation

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'brand', 'model', 'year', 'available']

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'user', 'car', 'start_date', 'end_date']

    def validate(self, data):
        if data['end_date'] < data['start_date']:
            raise serializers.ValidationError("End date must be after start date.")
        
        # Check if car is available for the specified dates
        reservations = Reservation.objects.filter(
            car=data['car'],
            start_date__lt=data['end_date'],
            end_date__gt=data['start_date']
        )
        if reservations.exists():
            raise serializers.ValidationError("This car is already reserved for the selected dates.")
        return data
