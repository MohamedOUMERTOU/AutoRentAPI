from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Car, Reservation
from .serializers import CarSerializer, ReservationSerializer
from django.shortcuts import get_object_or_404
class CarListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cars = Car.objects.filter(available=True)
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)

class CarDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        car = Car.objects.get(id=id)
        serializer = CarSerializer(car)
        return Response(serializer.data)

class CarCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class CarUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        serializer = CarSerializer(car, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CarDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserReservationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        if request.user.id != user_id:
            return Response({"error": "Unauthorized access to reservations"}, status=status.HTTP_403_FORBIDDEN)
        
        reservations = Reservation.objects.filter(user_id=user_id)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

class ReservationUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        reservation = Reservation.objects.get(id=id, user=request.user)
        serializer = ReservationSerializer(reservation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReservationDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        reservation = Reservation.objects.get(id=id, user=request.user)
        reservation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
class ReservationCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Validate the reservation's dates and availability
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')

        if start_date >= end_date:
            return Response({"error": "End date cannot be earlier than start date."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if car is available for the given period
        car_id = request.data.get('car')
        car = get_object_or_404(Car, id=car_id)
        conflicting_reservation = Reservation.objects.filter(
            car=car,
            start_date__lt=end_date,
            end_date__gt=start_date
        ).exists()

        if conflicting_reservation:
            return Response({"error": "Car is already reserved for the given dates."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
