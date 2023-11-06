from rest_framework import serializers
from django.contrib.auth import authenticate, password_validation
from rest_framework_simplejwt.tokens import RefreshToken
from dashboard.models.user_model import CustomUser, RecoverPassword
from django.utils import timezone
from datetime import datetime, timedelta
from dashboard.tasks import send_notification_email_task, send_email_otp_task, send_password_reset_notification_task
from dashboard.utils.machine.get_data_machine import get_client_info
from dashboard.utils.location.get_location_info import get_location_info
from dashboard.utils.otp_handler import create_or_update_recovery_data
import logging

logger = logging.getLogger(__name__)

MAX_FAILED_ATTEMPTS = 5 
LOCKOUT_TIME = 30

class AuthUserRegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(label='First Name', max_length=30)
    last_name = serializers.CharField(label='Last Name', max_length=30)
    email = serializers.EmailField(label='E-mail', max_length=254)
    password = serializers.CharField(
        label="Password",
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        min_length=8,
        max_length=128,
        validators=[password_validation.validate_password]
    )
    passconf = serializers.CharField(
        label="Confirm Password",
        write_only=True,
        style={'input_type': 'password'},
        min_length=8,
        max_length=128,
        required=True
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password', 'passconf']

    def is_valid(self, raise_exception=False):
        is_valid = super(AuthUserRegisterSerializer, self).is_valid(raise_exception=False)

        if not is_valid and 'non_field_errors' in self.errors:
            custom_errors = {}
            custom_errors['error'] = self.errors['non_field_errors'][0]
            self._errors = custom_errors

            if raise_exception:
                raise serializers.ValidationError(self.errors)

        return is_valid

    def validate(self, data):
        if data.get('password') != data.get('passconf'):
            raise serializers.ValidationError('As senhas não coincidem.')

        email = data.get('email')

        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Endereço de email já está em uso.')

        return data

    def create(self, validated_data):
        validated_data.pop('passconf')

        ip_address = self.context['request'].META.get('REMOTE_ADDR')
        machine_info = get_client_info(self.context['request'])
        location_info = get_location_info(ip_address)

        user = CustomUser.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        send_notification_email_task.delay(validated_data['email'], machine_info, location_info)

        return user



class AuthUserSignInSerializer(serializers.Serializer):
    email = serializers.EmailField(label='E-mail', max_length=254)
    password = serializers.CharField(
        label="Password",
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        min_length=8,
        max_length=128,
        validators=[password_validation.validate_password]
    )

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = CustomUser.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError("E-mail não registrado.")

        user_authenticated = authenticate(username=email, password=password)

        if user_authenticated:
            user.failed_login_attempts = 0
            user.save()
            refresh = RefreshToken.for_user(user)
            response_data = {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'token': str(refresh.access_token),
                'refresh': str(refresh), 
            }
            return response_data
        else:
            user.failed_login_attempts += 1
            user.last_failed_login = datetime.now()
            user.save()

            if user.failed_login_attempts >= MAX_FAILED_ATTEMPTS:
                lockout_time = timedelta(minutes=LOCKOUT_TIME)
                current_time = datetime.now()

                if user.last_failed_login and (current_time - user.last_failed_login) > lockout_time:
                    user.failed_login_attempts = 0
                    user.save()
                else:
                    logger.info("Muitas tentativas de login. Tente novamente em {} minutos.".format(LOCKOUT_TIME))
                    raise serializers.ValidationError("Muitas tentativas de login. Tente novamente em {} minutos.".format(LOCKOUT_TIME))

            raise serializers.ValidationError("Unable to log in with provided credentials.",code='authentication_failed')



class AuthUserRecoverySerializer(serializers.Serializer):
    email = serializers.EmailField(label='E-mail', max_length=254)

    def validate_email(self, value):
        user = CustomUser.objects.filter(email=value).first()
        if not user:
            raise serializers.ValidationError('E-mail não encontrado')

        ip_address = self.context['request'].META.get('REMOTE_ADDR')
        device_info = get_client_info(self.context['request'])
        location_info = get_location_info(ip_address)
        recovery_data = create_or_update_recovery_data(user, ip_address, device_info)
        
        send_email_otp_task.delay(value, recovery_data.otp, device_info, location_info)

        return value

    def create(self, validated_data):
        return validated_data



class AuthUserOtpSerializer(serializers.Serializer):
    otp = serializers.CharField(label="One-Time Password", max_length=6, write_only=True)

    class Meta:
        model = RecoverPassword
        fields = ('otp',)

    def validate(self, data):
        try:
            otp_data = RecoverPassword.objects.get(otp=data['otp'])
        except RecoverPassword.DoesNotExist:
            raise serializers.ValidationError('O OTP é inválido.')

        if otp_data.is_used:
            raise serializers.ValidationError('Este OTP já foi utilizado.')

        # Calculando a diferença de tempo entre agora e a criação do OTP
        current_time = timezone.now()
        time_difference = current_time - otp_data.expiry_datetime

        # Logging
        logger.info(f"Expiry DateTime for OTP: {otp_data.expiry_datetime}")
        logger.info(f"Current DateTime: {current_time}")
        logger.info(f"Time Difference: {time_difference}")

        # Verificar se a diferença de tempo é maior que 10 minutos
        if time_difference > timedelta(hours=1):
            raise serializers.ValidationError('O OTP expirou.')

        token_value = f"{str(otp_data.id)}/{otp_data.token}"
        logger.info(f"Token Value: {token_value}")
        return {"token": token_value}

#########################################################
class AuthUserResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        label="Password",
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        min_length=8,
        max_length=128,
        validators=[password_validation.validate_password]
    )
    passconf = serializers.CharField(
        label="Confirm Password",
        write_only=True,
        style={'input_type': 'password'},
        min_length=8,
        max_length=128,
        required=True
    )

    def validate(self, data):
        if data['password'] != data['passconf']:
            raise serializers.ValidationError("As senhas não correspondem.")
        return data

    def update(self, instance, validated_data):
        instance.user.set_password(validated_data['password'])
        instance.user.save()

        instance.is_used = True
        instance.expiry_datetime = timezone.now()
        instance.save()

        # Enviar notificação de e-mail
        ip_address = self.context['request'].META.get('REMOTE_ADDR')
        device_info = get_client_info(self.context['request'])
        location_info = get_location_info(ip_address)
        
        send_password_reset_notification_task.delay(instance.user.email, device_info, location_info)

        return instance

