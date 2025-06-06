from django.urls import path
from .views import list_classes, book_slot, get_bookings

urlpatterns = [
    path("classes/", list_classes, name="list_classes"),
    path("book/", book_slot, name="book_slot"),
    path("bookings/", get_bookings, name="get_bookings"),
]
