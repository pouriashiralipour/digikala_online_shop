from django.contrib import messages
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import RegisterForm
from .models import CustomUser
from .otp_sender import check_otp_time, get_random_otp, send_otp, send_otp_soap


def register_view(request):
    form = RegisterForm()
    if request.method == "POST":
        phone_number = request.POST.get("phone_number")
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
            # کاربر موجود است، ارسال OTP برای ورود
            otp = get_random_otp()
            # send_otp_soap(phone_number, otp)
            # send_otp(phone_number, otp)
            user.otp = otp
            print(otp)
            user.save()
            request.session["user_number"] = user.phone_number
            return HttpResponseRedirect(reverse("verify_view"))
        except CustomUser.DoesNotExist:
            # کاربر جدید است، ثبت نام و ارسال OTP
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                otp = get_random_otp()
                # send_otp_soap(phone_number, otp)
                # send_otp(phone_number, otp)
                user.otp = otp
                print(otp)
                user.is_active = False
                user.save()
                request.session["user_number"] = user.phone_number
                request.session["is_new_user"] = True
                return HttpResponseRedirect(reverse("verify_view"))
    return render(request, "registration/login-register.html", {"form": form})


def welcome_view(request):
    return render(request, "registration/welcome.html")


def verify_view(request):
    try:
        phone_number = request.session.get("user_number")
        user = CustomUser.objects.get(phone_number=phone_number)
        if request.method == "POST":
            # check otp time
            if not check_otp_time(user.phone_number):
                messages.error(request, "OTP is expired, please try again.")
                return HttpResponseRedirect(reverse("register_view"))
            if user.otp != int(request.POST.get("otp")):
                messages.error(request, "OTP is incorrect.")
                return HttpResponseRedirect(reverse("register_view"))
            user.is_active = True
            user.save()
            login(request, user)
            if request.session.get("is_new_user"):
                del request.session["is_new_user"]
                return HttpResponseRedirect(reverse("welcome_view"))
            else:
                return HttpResponseRedirect(reverse("home_page"))
        return render(
            request, "registration/verification.html", {"phone_number": phone_number}
        )
    except CustomUser.DoesNotExist:
        messages.error(request, "Error occurred, try again.")
        return HttpResponseRedirect(reverse("register_view"))
