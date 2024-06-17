from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import CustomUserCreationForm
from .models import CustomUser


def register_view(request):
    form = CustomUserCreationForm
    if request.method == "POST":
        try:
            if "phone_number" in request.POST:
                phone_number = request.POST.get("phone_number")
                user = CustomUser.objects.get(phone_number=phone_number)
                # send otp
                # save otp
                user.save()
                # redirect to vrify page
        except CustomUser.DoesNotExist:
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                # send otp
                # save otp
                user.is_active = False
                user.save()
                # redirect to vrify page
    return render(request, "login_signup.html", {"form": form})


# def mobile_login_view(request):
#     if request.method == "POST":
#         if "phone_number" in request.POST:
#             phone_number = request.POST.get("phone_number")
#             user = CustomUser.objects.get(phone_number=phone_number)
#             login(request, user)
#             return HttpResponseRedirect(reverse("dashboard"))
#     return render(request, "login_signup.html")


def dashboard_view(request):
    return render(request, "dashboard.html")
