from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import CustomUser


def mobile_login_view(request):
    if request.method == "POST":
        if "phone_number" in request.POST:
            phone_number = request.POST.get("phone_number")
            user = CustomUser.objects.get(phone_number=phone_number)
            login(request, user)
            return HttpResponseRedirect(reverse("dashboard"))
    return render(request, "login_signup.html")


def dashboard_view(request):
    return render(request, "dashboard.html")
