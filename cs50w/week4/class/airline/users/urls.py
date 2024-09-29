from django. urls import path

from . import views

urlpatterns = [
    path(route='', view=views.index, name='index'),
    path(route='login', view=views.login_view, name='login'),
    path(route='logout', view=views.logout_view, name='logout')
]