from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser


class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            "phone_number",
        ]
