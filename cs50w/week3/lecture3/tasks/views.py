from django.shortcuts import render
from django.http import HttpRequest

tasks = ["foo", "bar", "baz"]

def index(request: HttpRequest):
    return render(
        request=request,
        template_name="tasks/index.html",
        context={
            "tasks": tasks
        }
    )