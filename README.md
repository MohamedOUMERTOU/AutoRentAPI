# AutoRentAPI
AutoRentAPI is a RESTful API for a car rental service that allows users to browse available cars, create reservations, view their own bookings, and modify or cancel reservations. Built with Django and Django REST Framework, this project includes key functionalities to ensure secure and efficient booking management:
User Authentication: Secured endpoints with JWT tokens to ensure user identity and data privacy.
Car Availability: Validates that cars are not double-booked for overlapping dates.
Reservation Validations: Ensures reservation dates are consistent, with checks to avoid incorrect date ranges.
Endpoints:
#GET /api/cars: List available cars
#GET /api/cars/{id}: View car details
#POST /api/reservations: Create a reservation
#GET /api/users/{id}/reservations: View user's reservations
#PUT /api/reservations/{id}: Update a reservation
#DELETE /api/reservations/{id}: Cancel a reservation
This project is ideal for developers looking to understand secure booking systems, date validations, and Django REST API design.


login :adminauto
pwd:adminauto