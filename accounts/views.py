from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect, JsonResponse
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
            user.otp = otp
            print(otp)
            user.save()
            request.session["user_number"] = user.phone_number
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse(
                    {"success": True, "redirect_url": reverse("verify_view")}
                )
            return HttpResponseRedirect(reverse("verify_view"))
        except CustomUser.DoesNotExist:
            # کاربر جدید است، ثبت نام و ارسال OTP
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                otp = get_random_otp()
                user.otp = otp
                print(otp)
                user.is_active = False
                user.save()
                request.session["user_number"] = user.phone_number
                request.session["is_new_user"] = True
                if request.headers.get("x-requested-with") == "XMLHttpRequest":
                    return JsonResponse(
                        {"success": True, "redirect_url": reverse("verify_view")}
                    )
                return HttpResponseRedirect(reverse("verify_view"))
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"success": False, "message": "Invalid form data"})
    return render(request, "registration/login-register.html", {"form": form})


def welcome_view(request):
    return render(request, "registration/welcome.html")


def verify_view(request):
    try:
        phone_number = request.session.get("user_number")
        user = CustomUser.objects.get(phone_number=phone_number)
        if request.method == "POST":
            # بررسی زمان انقضای OTP
            if not check_otp_time(user.phone_number):
                message = "OTP is expired, please try again."
                if request.headers.get("x-requested-with") == "XMLHttpRequest":
                    return JsonResponse({"success": False, "message": message})
                messages.error(request, message)
                return HttpResponseRedirect(reverse("register_view"))
            if user.otp != int(request.POST.get("otp")):
                message = "OTP is incorrect."
                if request.headers.get("x-requested-with") == "XMLHttpRequest":
                    return JsonResponse({"success": False, "message": message})
                messages.error(request, message)
                return HttpResponseRedirect(reverse("register_view"))
            user.is_active = True
            user.save()
            login(request, user)
            if request.session.get("is_new_user"):
                del request.session["is_new_user"]
                redirect_url = reverse("welcome_view")
            else:
                redirect_url = reverse("home_page")
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"success": True, "redirect_url": redirect_url})
            return HttpResponseRedirect(redirect_url)
        return render(
            request, "registration/verification.html", {"phone_number": phone_number}
        )
    except CustomUser.DoesNotExist:
        message = "Error occurred, try again."
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": False, "message": message})
        messages.error(request, message)
        return HttpResponseRedirect(reverse("register_view"))


def logout_view(request):
    logout(request)
    return redirect("home_page")
