from django.core.mail import send_mail
from django.conf import settings

def send_result_upload_notification(email, subject, message):
    if not settings.EMAIL_HOST or not settings.DEFAULT_FROM_EMAIL:
        raise EnvironmentError("Email backend is not configured properly.")

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False
    )