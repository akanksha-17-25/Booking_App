from rest_framework import serializers
from django.utils import timezone
from .models import Class, Slot, Booking, Client


class SlotSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Slot
        fields = ['id', 'seats', 'start_time', 'end_time', ]


class ClassSerializer(serializers.ModelSerializer):
    slots = serializers.SerializerMethodField()


    def get_slots(self, obj):
        # Filter slots to only include future ones
        future_slots = obj.slots.filter(start_time__gt=timezone.now())
        return SlotSerializer(future_slots, many=True).data
    

   

    class Meta:
        model = Class
        fields = ['id', 'name', 'instructor', 'slots'] 

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'email']

class ClassWithoutSlotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['id', 'name', 'instructor']

class SlotWithClassSerializer(serializers.ModelSerializer):
    class_id = ClassWithoutSlotsSerializer()
    class Meta:
        model = Slot
        fields = ['id', 'seats', 'start_time', 'end_time', 'class_id']

class BookingRequestSerializer(serializers.Serializer):
    slot_id = serializers.IntegerField(required=True)
    client_email = serializers.EmailField(required=True)
    client_name = serializers.CharField(required=True, max_length=255)

class BookingSerializer(serializers.ModelSerializer):
    client = ClientSerializer() 
    slot = SlotWithClassSerializer()
    class Meta:
        model = Booking
        fields = ['id', 'client', 'slot']