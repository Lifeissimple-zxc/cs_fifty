from django.shortcuts import render
from django.http import HttpRequest

from .models import Flight

# Create your views here.
def index(request: HttpRequest):
    return render(
        request=request,
        template_name="flights/index.html",
        context={
            "flights": Flight.objects.all()
        }
    )

def flight(request: HttpRequest, flight_id: int):
    f = Flight.objects.get(pk=flight_id)
    return render(
        request=request,
        template_name="flights/flight.html",
        context={
            "flight": f,
            # this is possible thanks to related_name attr
            "passengers": f.passengers.all()
        }
    )