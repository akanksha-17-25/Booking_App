from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from .models import Class, Slot, Client, Booking


class BookingFlowTests(APITestCase):

    def setUp(self):
        self.class_obj = Class.objects.create(name="Yoga", instructor="Alice")
        self.slot = Slot.objects.create(
            class_id=self.class_obj,
            seats=2,
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=1)
        )
        self.client_data = {
            "email": "john@example.com",
            "name": "John Doe"
        }
        self.client_request_data = {
            "client_email": self.client_data["email"],
            "client_name": self.client_data["name"],
        }


    def test_list_classes(self):
        response = self.client.get("/api/classes/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        # @todo: test data name and instructor

    def test_book_slot_success(self):
        response = self.client.post("/api/book/", {
            "slot_id": self.slot.id,
            **self.client_request_data
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Slot booked successfully")
        self.slot.refresh_from_db()
        self.assertEqual(self.slot.seats, 1)  # because 1 seat is booked

    def test_book_slot_already_booked(self):
        # First booking
        self.client.post("/api/book/", {
            "slot_id": self.slot.id,
            **self.client_request_data

        })
        # Second booking attempt
        response = self.client.post("/api/book/", {
            "slot_id": self.slot.id,
            **self.client_request_data
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Client already booked")

    def test_book_slot_no_seats(self):
        self.slot.seats = 0
        self.slot.save()
        response = self.client.post("/api/book/", {
            "slot_id": self.slot.id,
            **self.client_request_data
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "No free seats")

    def test_get_bookings_success(self):
        client = Client.objects.create(**self.client_data)
        Booking.objects.create(client=client, slot=self.slot)
        response = self.client.get(f"/api/bookings/?email={client.email}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['client']['email'], client.email)

    def test_get_bookings_no_email(self):
        response = self.client.get("/api/bookings/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Email is required")
