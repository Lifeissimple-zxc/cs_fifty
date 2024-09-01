from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from django import forms, urls


TASKS_KEY = "tasks"


class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")
    priority = forms.IntegerField(label="Priority", min_value=1, max_value=10)

def index(request: HttpRequest):
    # per user task list (session based)
    if TASKS_KEY not in request.session:
        request.session[TASKS_KEY] = []
    return render(
        request=request,
        template_name="tasks/index.html",
        context={
            "tasks": request.session[TASKS_KEY]
        }
    )

def add(request: HttpRequest):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            request.session[TASKS_KEY] += [form.cleaned_data["task"]]
            return HttpResponseRedirect(
                urls.reverse(viewname="tasks:index")
            )
        return render(
            request=request,
            template_name="tasks/add.html",
            context={"form": form}
        )

    return render(
        request=request,
        template_name="tasks/add.html",
        context={"form": NewTaskForm()}
    )