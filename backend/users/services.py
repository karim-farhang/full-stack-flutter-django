from django.core.mail import send_mail
from django.conf import settings

def send_otp_email(email: str, code: str):
    send_mail(
        subject="Your OTP Code",
        message=f"Your OTP code is: {code}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
