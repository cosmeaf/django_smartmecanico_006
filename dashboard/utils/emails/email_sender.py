from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_notification_email(email, device_info, location_info):
    subject = 'Conta Criada no Sistema XPTO'
    
    try:
        message = (
            f"Olá,\n\n"
            f"Uma nova conta foi criada com o e-mail: {email} no Sistema XPTO.\n\n"
            f"Informações da máquina:\n"
            f"Browser: {device_info['browser']}\n"
            f"Versão do Browser: {device_info.get('browser_version', 'Não informado')}\n"
            f"Dispositivo: {device_info['device']}\n"
            f"Sistema Operacional: {device_info['os_name']}\n"
            f"Versão do Sistema Operacional: {device_info['os_version']}\n\n"
            f"Informações de localização:\n"
            f"IP: {location_info['ip']}\n"
            f"ISP: {location_info['isp']}\n"
            f"País: {location_info['country']}\n"
            f"Estado: {location_info['state']}\n"
            f"Cidade: {location_info['city']}\n"
            f"Código Postal: {location_info['zipcode']}\n"
        )
        send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)

        logger.info("E-mail enviado com sucesso.")
        return True
    except BadHeaderError:  
        logger.error("Erro nos headers do e-mail.")
        return False
    except Exception as e:
        logger.error(f"Erro ao enviar e-mail: {e}")
        return False


def send_email_otp(user_email, otp_code, device_info, location_info):
    subject = 'Solicitação de Recuperação de Senha no Sistema XPTO'
    
    try:
        message = (
            f"Olá,\n\n"
            f"Foi realizada uma solicitação de recuperação de senha para o e-mail: {user_email} no Sistema XPTO.\n\n"
            f"Seu código OTP é: {otp_code}\n\n"
            f"Informações da máquina:\n"
            f"Browser: {device_info.get('browser', 'Não informado')}\n"
            f"Dispositivo: {device_info.get('device', 'Não informado')}\n"
            f"Sistema Operacional: {device_info.get('os_name', 'Não informado')}\n"
            f"Versão do Sistema Operacional: {device_info.get('os_version', 'Não informado')}\n\n"
            f"Informações de localização:\n"
            f"IP: {location_info.get('ip', 'Não informado')}\n"
            f"ISP: {location_info.get('isp', 'Não informado')}\n"
            f"País: {location_info.get('country', 'Não informado')}\n"
            f"Estado: {location_info.get('state', 'Não informado')}\n"
            f"Cidade: {location_info.get('city', 'Não informado')}\n"
            f"Código Postal: {location_info.get('zipcode', 'Não informado')}\n"
        )
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email], fail_silently=False)

        logger.info("E-mail OTP enviado com sucesso.")
        return True
    except BadHeaderError:  
        logger.error("Erro nos headers do e-mail.")
        return False
    except Exception as e:
        logger.error(f"Erro ao enviar e-mail OTP: {e}")
        return False


def send_password_reset_notification_email(user_email, device_info, location_info):
    subject = 'Redefinição de Senha no Sistema XPTO'
    
    try:
        message = (
            f"Olá,\n\n"
            f"Sua senha foi redefinida com sucesso no Sistema XPTO.\n\n"
            f"Informações da máquina:\n"
            f"Browser: {device_info.get('browser', 'Não informado')}\n"
            f"Dispositivo: {device_info.get('device', 'Não informado')}\n"
            f"Sistema Operacional: {device_info.get('os_name', 'Não informado')}\n"
            f"Versão do Sistema Operacional: {device_info.get('os_version', 'Não informado')}\n\n"
            f"Informações de localização:\n"
            f"IP: {location_info.get('ip', 'Não informado')}\n"
            f"ISP: {location_info.get('isp', 'Não informado')}\n"
            f"País: {location_info.get('country', 'Não informado')}\n"
            f"Estado: {location_info.get('state', 'Não informado')}\n"
            f"Cidade: {location_info.get('city', 'Não informado')}\n"
            f"Código Postal: {location_info.get('zipcode', 'Não informado')}\n"
        )
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email], fail_silently=False)

        logger.info("E-mail de redefinição de senha enviado com sucesso.")
        return True
    except BadHeaderError:  
        logger.error("Erro nos headers do e-mail.")
        return False
    except Exception as e:
        logger.error(f"Erro ao enviar e-mail de redefinição de senha: {e}")
        return False