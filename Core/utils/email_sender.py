from django.core.mail import send_mail
from django.conf import settings

def send_result_upload_notification(email, subject, message):
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False
    )