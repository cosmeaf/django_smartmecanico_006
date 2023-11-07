# auth_user_otp_form.py

from django import forms
from django.utils import timezone
from datetime import timedelta
from dashboard.models.user_model import RecoverPassword
from django.core.exceptions import ValidationError

class AuthUserOtpForm(forms.Form):
    otp = forms.CharField(label="One-Time Password", max_length=6, widget=forms.TextInput(attrs={'type': 'number'}))

    def clean_otp(self):
        otp_value = self.cleaned_data.get('otp')

        try:
            otp_data = RecoverPassword.objects.get(otp=otp_value)
        except RecoverPassword.DoesNotExist:
            raise forms.ValidationError('O OTP é inválido.')

        if otp_data.is_used:
            raise forms.ValidationError('Este OTP já foi utilizado.')

        current_time = timezone.now()
        time_difference = current_time - otp_data.expiry_datetime

        if time_difference > timedelta(hours=1):
            raise forms.ValidationError('O OTP expirou.')

        token_value = f"{str(otp_data.id)}/{otp_data.token}"
        return token_value
