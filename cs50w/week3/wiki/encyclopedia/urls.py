from django.urls import path

from . import views

urlpatterns = [
    
    path(route="", view=views.index, name="index"),
    path(route="wiki/<str:title>", view=views.title, name="title"),
    path(route="random_entry", view=views.random_entry, name="random"),
    path(route="search_entry", view=views.search_entry, name="search_entry")
]
