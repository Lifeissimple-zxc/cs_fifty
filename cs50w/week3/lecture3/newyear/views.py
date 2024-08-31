from datetime import datetime, timezone

from django.shortcuts import render
from django.http import HttpRequest

# Create your views here.
def index(request: HttpRequest):
    now = datetime.now(tz=timezone.utc)
    return render(
        request=request,
        template_name="newyear/index.html",
        context={
            "newyear": now.day == 1 and now.month == 1
        }
    )