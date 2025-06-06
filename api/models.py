from django.db import models

# Create your models here.

class Class(models.Model):
    name = models.CharField(max_length=100)
    instructor = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name} - {self.instructor}"
    
    class Meta:
        verbose_name_plural = "Classes"



class Client(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name} ({self.email})"


class Slot(models.Model):
    seats = models.PositiveIntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='slots')
    
    def __str__(self):
        return f"{self.class_id.name} - {self.start_time} to {self.end_time}"
    
   


class Booking(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='bookings')
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE, related_name='bookings')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.client.name} - {self.slot.class_id.name} ({self.slot.start_time})"
    
    class Meta:
        unique_together = ('client', 'slot')  # Prevent duplicate bookings
