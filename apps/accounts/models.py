from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from apps.accounts.managers import UserManager
from apps.utils.base_model import BaseModel


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True, verbose_name="Email")
    phone_number = models.CharField(max_length=11, unique=True, verbose_name="Phone Number")
    full_name = models.CharField(max_length=255, verbose_name="Full Name")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    is_admin = models.BooleanField(default=False, verbose_name="Admin")

    USERNAME_FIELD = 'phone_number'  # field for authenticate users
    REQUIRED_FIELDS = ['email', 'full_name']  # used just in createsuperuser command

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class OtpCode(BaseModel):
    phone_number = models.CharField(max_length=11, verbose_name="Phone Number")
    code = models.PositiveSmallIntegerField(verbose_name="OTP Code")

    def __str__(self):
        return f'{self.phone_number} - {self.code} - {self.created_at}'

    class Meta:
        db_table = 'otp_code'
        verbose_name = 'OTP Code'
        verbose_name_plural = 'OTP Codes'
