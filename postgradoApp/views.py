from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils.decorators import method_decorator
from django.contrib import messages

@login_required
def index(request):
    return render(request,"index.html")


def exit(request):
    logout(request)
    return redirect("index.html")

