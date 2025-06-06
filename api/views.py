from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db import transaction, connection
from django.db.models import F
import pprint
# Create your views here.
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import Class, Slot, Booking, Client
from .serializers import ClassSerializer, BookingSerializer, BookingRequestSerializer


@api_view(["GET"])
def list_classes(request):
    # Select only classes that have future slots
    classes = Class.objects.all()
    serializer = ClassSerializer(classes, many=True)
    return Response(serializer.data)

@api_view(["POST"])
def book_slot(request):
    # edge cases:
    #   no free seats
    #   client already booked
    #   if client doesn't exist, create one or fetch from DB if exists
    #   race condition
    

    serializer = BookingRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
        
    
    slot_id = serializer.validated_data.get("slot_id")
    client_email = serializer.validated_data.get("client_email")
    client_name = serializer.validated_data.get("client_name")
    
    # transaction to avoid race condition
    with transaction.atomic():
        try:
            slot = Slot.objects.select_for_update().get(id=slot_id)
        except Slot.DoesNotExist:
            raise NotFound("Invalid slot_id")
        
        # Check if any seat is left
        if slot.seats <= 0:
            return Response({"message": "No free seats"}, status=400)

        # Get or create client
        client, created = Client.objects.get_or_create(email=client_email, defaults={"name": client_name})

        # Check if already booked
        if (not created) and Booking.objects.filter(slot=slot, client=client).exists():
            return Response({"message": "Client already booked"}, status=400)

        # Book and reduce seat
        # UPDATE slot SET seats = 49 WHERE id = slot_id;
        # slot.seats -= 1
        # UPDATE booking SET seats = seats - 1 WHERE id = slot_id;
        # SELECT * FROM slot WHERE id = user_id
        # Slot.objects.filter(id=user_id)
        # Slot.objects.filter(id=F("user_id"))
        slot.seats = F("seats") - 1
        slot.save()

        booking = Booking.objects.create(slot=slot, client=client)

    return Response({"message": "Slot booked successfully"})


@api_view(["GET"])
def get_bookings(request):
    email = request.query_params.get("email")
    if not email:
        return Response({"message": "Email is required"}, status=400)
    # select_related to avoid N+1 queries
    bookings = Booking.objects.filter(client__email=email).select_related('client', 'slot', 'slot__class_id')

    res = Response(BookingSerializer(bookings, many=True).data)
    # uncomment to see the queries
    pprint.pprint(connection.queries)
    return res