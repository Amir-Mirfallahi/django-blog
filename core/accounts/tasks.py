from celery import shared_task


@shared_task
def send_email(email_obj):
    email_obj.send()