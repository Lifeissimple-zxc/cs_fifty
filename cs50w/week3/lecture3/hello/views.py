from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request: HttpRequest):
    return render(request=request, template_name="hello/index.html")

def man(request: HttpRequest):
    return HttpResponse("Hello Man!")

def greet(request: HttpRequest, name: str):
    return render(
        request=request,
        template_name="hello/greet.html",
        context={
            "name": name.capitalize()
        }
    )


