from celery import shared_task

from apps.accounts.services import KavenegarService


@shared_task
def send_otp_code_task(phone_number, otp_code):
    KavenegarService.get_instance().send_otp_code(phone_number, otp_code)
