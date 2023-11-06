# security/utils/otp_handler.py
import random
import base64
import uuid
import os
from datetime import datetime, timedelta
from django.utils import timezone
from dashboard.models.user_model import RecoverPassword
import logging

logger = logging.getLogger(__name__)

def generate_otp_code():
    return str(random.randint(100000, 999999))

def generate_token():
    return base64.urlsafe_b64encode(os.urandom(30)).decode('utf-8')

def create_or_update_recovery_data(user, ip_address, device_info):
    otp_code = generate_otp_code()
    token = generate_token()

    current_datetime = timezone.now()
    expiry_datetime = current_datetime + timezone.timedelta(hours=1)

    # Adicionando logs aqui
    logger.info(f"Current DateTime: {current_datetime}")
    logger.info(f"OTP Expiry DateTime: {expiry_datetime}")

    recovery_data, created = RecoverPassword.objects.update_or_create(
        user=user, 
        defaults={
            'otp': otp_code, 
            'expiry_datetime': expiry_datetime, 
            'token': uuid.uuid4(), 
            'ip_address': ip_address,
            'browser': device_info.get('browser', None),
            'device': device_info.get('device', None),
            'os_name': device_info.get('os_name', None),
            'os_version': device_info.get('os_version', None),
            'is_used': False
        }
    )

    return recovery_data