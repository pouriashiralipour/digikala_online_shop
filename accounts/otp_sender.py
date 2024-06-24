import datetime
import time
from random import randint

from django.conf import settings
from kavenegar import *
from zeep import Client

from .models import CustomUser


def send_otp(phone_number, otp):
    phone_number = [
        phone_number,
    ]
    try:
        api = KavenegarAPI(settings.KAVEHNEGAR_API)
        params = {
            "sender": "",  # optional
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


def send_otp_soap(phone_number, otp):
    time.sleep(10)
    client = Client("http://api.kavenegar.com/soap/v1.asmx?WSDL")
    receptor = [
        phone_number,
    ]
    empty_array_placeholder = client.get_type("ns0:ArrayOfString")
    receptors = empty_array_placeholder()
    for item in receptor:
        receptors["string"].append(item)
    api_key = settings.KAVEHNEGAR_API
    message = "Your OTP is {}".format(otp)
    sender = "10008663"
    status = 0
    status_message = ""
    result = client.service.SendSimpleByApikey(
        api_key,
        sender,
        message,
        receptors,
        0,
        1,
        status,
        status_message,
    )
    print(result)
    print("OTP", otp)


def get_random_otp():
    return randint(1000, 9999)


def check_otp_time(phone_number):
    try:
        user = CustomUser.objects.get(phone_number=phone_number)
        now = datetime.datetime.now()
        otp_datetime_created = user.otp_datetime_created
        diff_time = now - otp_datetime_created
        print("OTP_TIME : ", diff_time)
        if diff_time.seconds > 120:
            return False
        return True
    except CustomUser.DoesNotExist:
        return False
