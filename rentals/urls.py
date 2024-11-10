from django.urls import path
from .views import CarListView,CarCreateView, CarDetailView,CarDeleteView,CarUpdateView, ReservationCreateView, UserReservationsView, ReservationUpdateView, ReservationDeleteView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path('cars', CarListView.as_view(), name='car-list'),
    path('cars/<int:id>', CarDetailView.as_view(), name='car-detail'),
    path('cars/new/', CarCreateView.as_view(), name='car_create'),
    path('cars/<int:pk>/edit/', CarUpdateView.as_view(), name='car_edit'),
    path('cars/<int:pk>/delete/', CarDeleteView.as_view(), name='car_delete'),
    path('reservations', ReservationCreateView.as_view(), name='reservation-create'),
    path('users/<int:user_id>/reservations', UserReservationsView.as_view(), name='user-reservations'),
    path('reservations/<int:id>', ReservationUpdateView.as_view(), name='reservation-update'),
    path('reservations/<int:id>', ReservationDeleteView.as_view(), name='reservation-delete'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
