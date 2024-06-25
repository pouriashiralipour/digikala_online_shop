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
            else:
                if request.headers.get("x-requested-with") == "XMLHttpRequest":
                    errors = {
                        field: [str(error) for error in form.errors[field]]
                        for field in form.errors
                    }
                    return JsonResponse({"success": False, "errors": errors})
    return render(request, "registration/login-register.html", {"form": form})


def welcome_view(request):
    return render(request, "registration/welcome.html")


def verify_view(request):
    try:
        phone_number = request.session.get("user_number")
        user = CustomUser.objects.get(phone_number=phone_number)
        if request.method == "POST":
            otp_input = request.POST.get("otp")
            try:
                otp = int(otp_input)
            except (ValueError, TypeError):
                message = "لطفا کد تایید را وارد کنید."
                if request.headers.get("x-requested-with") == "XMLHttpRequest":
                    return JsonResponse({"success": False, "message": message})
                messages.error(request, message)
                return HttpResponseRedirect(reverse("verify_view"))

            # بررسی زمان انقضای OTP
            if not check_otp_time(user.phone_number):
                message = "کد تایید منقضی شده است."
                if request.headers.get("x-requested-with") == "XMLHttpRequest":
                    return JsonResponse({"success": False, "message": message})
                messages.error(request, message)
                return HttpResponseRedirect(reverse("verify_view"))

            if user.otp != otp:
                message = "کد تایید اشتباه است."
                if request.headers.get("x-requested-with") == "XMLHttpRequest":
                    return JsonResponse({"success": False, "message": message})
                messages.error(request, message)
                return HttpResponseRedirect(reverse("verify_view"))

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
        message = "خطایی رخ داد، لطفا مجددا تلاش کنید."
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": False, "message": message})
        messages.error(request, message)
        return HttpResponseRedirect(reverse("register_view"))


def logout_view(request):
    logout(request)
    return redirect("home_page")
