from celery import shared_task
import time
from django.core.mail import send_mail


@shared_task
def send_mail_task(subject, message):
    time.sleep(5)
    send_mail(subject, message, 'from@example.com',
              ['to@example.com'], fail_silently=False)