from celery import shared_task
from django.core.mail import send_mail

@shared_task
def cely_mail(title, body, sender, recievers):
    send_mail(title, body, sender, recievers)


