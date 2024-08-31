from django.shortcuts import render
from django.http import HttpRequest
from django import forms

tasks = ["foo", "bar", "baz"]


class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")
    priority = forms.IntegerField(label="Priority", min_value=1, max_value=10)

def index(request: HttpRequest):
    return render(
        request=request,
        template_name="tasks/index.html",
        context={
            "tasks": tasks
        }
    )

def add(request: HttpRequest):
    return render(
        request=request,
        template_name="tasks/add.html",
        context={
            "form": NewTaskForm()
        }
    )