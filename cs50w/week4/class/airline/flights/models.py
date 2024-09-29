from django.db import models

# Create your models here.
# model is a single DB table (simplified)
class Airport(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.city} ({self.code})"
    

class Flight(models.Model):
    # related_name adds a property to airports such that it stores all the related flights
    origin = models.ForeignKey(to=Airport, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(to=Airport, on_delete=models.CASCADE, related_name="arrivals")
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.id}: {self.origin} to {self.destination}. Duration: {self.duration}"
    

class Passenger(models.Model):
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    # related_name allows to fetch all passengers of a flight
    flights = models.ManyToManyField(to=Flight, blank=True, related_name="passengers")

    def __str__(self):
        return f"{self.first} {self.last}"
