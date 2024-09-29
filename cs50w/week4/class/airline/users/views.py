from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def index(request: HttpRequest):
    # provided by django!
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse(viewname="login"))
    return render(
        request=request,
        template_name="users/user.html"
    )
    
def login_view(request: HttpRequest):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request=request, username=username, password=password)
        if user is not None:
            login(request=request, user=user)
            return HttpResponseRedirect(reverse(viewname="index"))
        return render(
            request=request,
            template_name="users/login.html",
            context={
                "message": "Invalid Credentials"
            }
        )

    return render(
        request=request,
        template_name="users/login.html"
    )

def logout_view(request: HttpRequest):
    logout(request=request)
    return render(
        request=request,
        template_name="users/login.html",
        context={
            "message": "Logged Out."
        }
    )
