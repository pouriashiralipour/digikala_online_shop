from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.register_view, name="register_view"),
    path("verify/", views.verify_view, name="verify_view"),
    path("welcome/", views.welcome_view, name="welcome_view"),
]
