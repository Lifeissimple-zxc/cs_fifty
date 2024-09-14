from django.urls import path

from . import views

urlpatterns = [
    
    path(route="", view=views.index, name="index"),
    path(route="wiki/<str:title>", view=views.title, name="title"),
    path(route="random", view=views.random_page, name="random")
]
