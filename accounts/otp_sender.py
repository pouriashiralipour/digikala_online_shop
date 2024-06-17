from kavenegar import *


def send_otp(phone_number, otp):
    try:
        api = KavenegarAPI("Your APIKey", timeout=20)
        params = {
            "sender": "",  # optional
            "receptor": "",  # multiple mobile number, split by comma
            "message": "",
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)
    print("OTP", otp)
