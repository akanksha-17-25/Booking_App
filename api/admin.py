from django.contrib import admin
from .models import Class, Client, Slot, Booking

# Register your models here.

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'instructor')
    search_fields = ('name', 'instructor')
    list_filter = ('instructor',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')
    list_filter = ('name',)


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ('class_id', 'start_time', 'end_time', 'seats')
    list_filter = ('class_id', 'start_time')
    search_fields = ('class_id__name',)
    date_hierarchy = 'start_time'
    
    


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('client_id', 'slot_id', 'created_at')
    list_filter = ('created_at', 'slot_id__class_id')
    search_fields = ('client_id__name', 'client_id__email', 'slot_id__class_id__name')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
