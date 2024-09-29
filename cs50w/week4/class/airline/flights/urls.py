from django.urls import path

from . import views

urlpatterns = [
    path(route="", view=views.index, name="index"),
    path(route="<int:flight_id>", view=views.flight, name="flight"),
    path(route="<int:flight_id>/book", view=views.book, name="book"),
]