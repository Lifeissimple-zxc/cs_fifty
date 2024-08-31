from django.urls import path
from . import views

urlpatterns = [
    path(route="", view=views.index, name="index"),
    path(route="man", view=views.man, name="man"),
    path(route="<str:name>", view=views.greet, name="greet")
]