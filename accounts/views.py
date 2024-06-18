from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import RegisterForm
from .models import CustomUser
from .otp_sender import get_random_otp, send_otp, send_otp_soap


def register_view(request):
    form = RegisterForm
    if request.method == "POST":
        try:
            if "phone_number" in request.POST:
                phone_number = request.POST.get("phone_number")
                user = CustomUser.objects.get(phone_number=phone_number)
                # send otp
                otp = get_random_otp()
                # send_otp_soap(phone_number, otp)
                # send_otp(phone_number, otp)
                # save otp
                user.otp = otp
                user.save()
                request.session["user_number"] = user.phone_number
                # redirect to vrify page
                return HttpResponseRedirect(reverse("verify_view"))
        except CustomUser.DoesNotExist:
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                # send otp
                otp = get_random_otp()
                # send_otp(phone_number, otp)
                # send_otp_soap(phone_number, otp)
                # save otp
                user.otp = otp
                user.is_active = False
                user.save()
                request.session["user_number"] = user.phone_number
                # redirect to vrify page
                return HttpResponseRedirect(reverse("verify_view"))
    return render(request, "register.html", {"form": form})


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


def verify_view(request):
    phone_number = request.session.get("user_number")
    return render(request, "verify.html", {"phone_number": phone_number})
