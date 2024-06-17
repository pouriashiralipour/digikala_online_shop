from django.urls import path

from . import views

urlpatterns = [
    path("", views.register_view, name="register_view"),
    # path("login/", views.mobile_login_view, name="mobile_login"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
]
