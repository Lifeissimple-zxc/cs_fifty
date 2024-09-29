from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse

from .models import Flight, Passenger

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
            "passengers": f.passengers.all(),
            # this performs a SELECT WHERE
            "non_passengers": Passenger.objects.exclude(flights=f.id).all() 
        }
    )

def book(request: HttpRequest, flight_id: int):
    if request.method == "POST":
        f = Flight.objects.get(pk=flight_id)
        passenger = Passenger.objects.get(pk=int(request.POST["passenger"]))
        passenger.flights.add(f)
        return HttpResponseRedirect(
            reverse(viewname="flight", args=(f.id,))
        )
