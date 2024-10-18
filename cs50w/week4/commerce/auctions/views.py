from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse

from . import models, forms


def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = models.User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
def render_error(request: HttpRequest):
    return render(
        request=request,
        template_name="auctions/error.html"
    )

def _render_new_listing_page(request: HttpRequest):
    return render(
        request=request,
        template_name="auctions/new_listing.html",
        context={
            "form": forms.NewListingForm()
        }
    )

def _post_new_listing(request: HttpRequest):
    form = forms.NewListingForm(request.POST)
    if not form.is_valid():
        return render_error(request=request)
    listing = form.save(commit=False)
    listing.user = request.user
    listing.status = models.LISTING_STATUS_ACTIVE
    listing.save() # TODO error handling
    return redirect(to="index")
    


def new_listing(request: HttpRequest):
    if not request.user.is_authenticated:
        return render_error(request=request)
    
    if request.method == "GET":
        return _render_new_listing_page(request=request)
    elif request.method == "POST":
        return _post_new_listing(request=request)