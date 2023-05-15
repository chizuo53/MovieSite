from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from MovieSite.celery import app

from django.conf import settings

@app.task
def send_check_spider_email(userpk, code):
    user = User.objects.get(pk=userpk)
    if user.is_superuser:
        return
    superusers_with_email = User.objects.all()
    receiver_emails = []
    for superuser in superusers_with_email:
        try:
            validate_email(superuser.email)
        except ValidationError:
            pass
        else:
            receiver_emails.append(superuser.email)
    if receiver_emails:
        subject = f'用户: {user.username} 提交了新的爬虫代码等待检查'
        message = code
        send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER , recipient_list=receiver_emails, fail_silently=False)

