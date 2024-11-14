from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.utils.timezone import now

@shared_task
def send_course_update_email(subject, message, recipient_list):
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)

@shared_task(name="lms.tasks.deactivate_inactive_users")
def deactivate_inactive_users():
    User = get_user_model()
    one_month_ago = now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago, is_active=True)

    for user in inactive_users:
        user.is_active = False
        user.save()

    return f"{inactive_users.count()} users deactivated"
