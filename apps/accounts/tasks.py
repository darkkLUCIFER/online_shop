from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from apps.accounts.models import OtpCode
from apps.accounts.services import KavenegarService


@shared_task
def send_otp_code_task(phone_number, otp_code):
    KavenegarService.get_instance().send_otp_code(phone_number, otp_code)


@shared_task
def remove_expired_otp_codes_task():
    expired_time = timezone.now() - timedelta(minutes=2)

    OtpCode.objects.filter(created_at__lt=expired_time).delete()
