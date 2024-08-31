from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.
def index(req: HttpRequest):
    return HttpResponse("Hello, world!")

def man(req: HttpRequest):
    return HttpResponse("Hello Man!")

def greet(req: HttpRequest, name: str):
    return HttpResponse(f"Hello, {name.capitalize()}!")

