from django import forms
from django.core.validators import RegexValidator

from .models import CustomUser


class RegisterForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            "phone_number",
            "otp",
        ]

    phone_number = forms.CharField(
        error_messages={"required": "لطفاً شماره موبایل خود را وارد کنید."},
        validators=[
            RegexValidator(
                r"^\d{11}$",
                message="فرمت شماره موبایل صحیح نیست. لطفاً یک شماره 11 رقمی وارد کنید.",
            )
        ],
    )

    otp = forms.CharField(
        required=False,  # OTP فیلد اختیاری است
        validators=[RegexValidator(r"^\d*$", message="فقط عدد وارد کنید.")],
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if not phone_number.isdigit():
            raise forms.ValidationError("فقط عدد وارد کنید.")
        return phone_number

    def clean_otp(self):
        otp = self.cleaned_data.get("otp")
        if otp and not otp.isdigit():
            raise forms.ValidationError("فقط عدد وارد کنید.")
        return otp

    def clean(self):
        cleaned_data = super().clean()
        phone_number = cleaned_data.get("phone_number")
        otp = cleaned_data.get("otp")

        if phone_number and not phone_number.isdigit():
            self.add_error("phone_number", "فقط عدد وارد کنید.")

        if otp and not otp.isdigit():
            self.add_error("otp", "فقط عدد وارد کنید.")
