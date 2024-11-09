from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Car, Reservation
from .serializers import CarSerializer, ReservationSerializer

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

class ReservationCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
