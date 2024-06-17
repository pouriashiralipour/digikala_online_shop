from random import randint

from django.conf import settings
from kavenegar import *


def send_otp(phone_number, otp):
    phone_number = [
        phone_number,
    ]
    try:
        api = KavenegarAPI(settings.KAVEHNEGAR_API, timeout=20)
        params = {
            "sender": "1000596446",  # optional
            "receptor": "phone_number",  # multiple mobile number, split by comma
            "message": "Your OTP is {}".format(otp),
        }
        response = api.sms_send(params)
        print("OTP", otp)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


def get_random_otp():
    return randint(1000, 9999)
