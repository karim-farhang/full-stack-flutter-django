from django.core.mail import send_mail
from django.conf import settings

def send_email(subject: str, message: str, to: str):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[to],
        fail_silently=False,
    )

def send_otp_email(email: str, code: str):
    send_email("Your OTP Code", f"Your OTP code is: {code}", email)
