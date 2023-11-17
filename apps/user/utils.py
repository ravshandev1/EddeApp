import requests
from django.conf import settings


def verify(phone, code):
    headers = {
        "Authorization": settings.SMS_TOKEN}
    data = {
        'mobile_phone': phone,
        'message': f"Confirmation code from Edd Foot: {code}",
        'from': "Edd Foot",
        'callback_url': 'https://google.com/'
    }
    requests.post(url=settings.SMS_URL, data=data, headers=headers)
