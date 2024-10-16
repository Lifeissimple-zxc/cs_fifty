from django.urls import path

from . import views

urlpatterns = [
    path(route="", view=views.index, name="index"),
    path(route="login", view=views.login_view, name="login"),
    path(route="logout", view=views.logout_view, name="logout"),
    path(route="register", view=views.register, name="register"),
    path(route="new_listing", view=views.new_listing, name="new_listing")
]
