from django.contrib.auth.backends import ModelBackend

from .models import CustomUser


class CustomBackendPhoneNumber(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        phone_number = kwargs["phone_number"]
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
        except CustomUser.DoesNotExist:
            pass
