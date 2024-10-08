from django.core.management.base import BaseCommand
from datetime import timedelta
from django.utils import timezone

from apps.accounts.models import OtpCode


class Command(BaseCommand):
    help = 'Remove expired OTPs'

    def handle(self, *args, **options):
        expired_time = timezone.now() - timedelta(minutes=2)

        OtpCode.objects.filter(created_at__lt=expired_time).delete()

        self.stdout.write(self.style.SUCCESS('Successfully removed expired OTPs'))
