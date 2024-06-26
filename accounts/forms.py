from django import forms

from .models import CustomUser


class RegisterForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            "phone_number",
        ]

    phone_number = forms.CharField(
        error_messages={"required": "لطفاً شماره موبایل خود را وارد کنید."}
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if len(phone_number) != 11:
            raise forms.ValidationError("شماره موبایل را به درستی وارد کنید")
        return phone_number
