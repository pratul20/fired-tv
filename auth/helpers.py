import requests
import random

from django.conf import settings

def send_otp_to_phone(phone_number):
    try:
        otp = random.randint(1000,9999)
        url = f'https://2factor.in/API/V1/{settings.API_KEY_2FACTOR}/SMS/{phone_number}/{otp}'
        requests.get(url) # To send OTP to mobile number
        return otp
    except Exception as e:
        print(e)
        return None

