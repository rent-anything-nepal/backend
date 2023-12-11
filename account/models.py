import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from account.text_from_image import *
from account.validators import validate_citizenship_number
from backend.settings.base import RESET_PASSWORD_CODE_EXPIRE_TIME
from media.models import Timestamp


PROFILE_TYPE_CHOICES = ((1, "Seeker"), (2, "Owner"), (3, "Maintainer"))


def upload_citizenship_back_to(instance, filename):
    ext = filename.split(".")[-1]
    return f"citizenship_back/{uuid.uuid4()}.{ext}"


def upload_avatar_to(instance, filename):
    ext = filename.split(".")[-1]
    return f"avatar/{uuid.uuid4()}.{ext}"


class Profile(Timestamp):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, editable=False)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    primary_contact = models.CharField(max_length=255)
    secondary_contact = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    account_type = models.PositiveIntegerField(choices=PROFILE_TYPE_CHOICES, default=1)
    citizenship_number = models.CharField(
        max_length=255, null=True, validators=[validate_citizenship_number], unique=True, editable=False
    )
    citizenship_back = models.ImageField(null=True, upload_to=upload_citizenship_back_to)
    is_citizenship_verified = models.BooleanField(default=False, editable=False)
    is_contact_verified = models.BooleanField(default=False, editable=False)
    is_email_verified = models.BooleanField(default=False, editable=False)
    avatar = models.ImageField(null=True, upload_to=upload_avatar_to)

    @property
    def is_profile_verified(self):
        if self.account_type == 2:
            return self.is_citizenship_verified and self.is_contact_verified
        else:
            return self.is_contact_verified and self.is_email_verified

    @property
    def full_name(self):
        full_name = self.user.first_name
        if self.middle_name:
            full_name += f" {self.middle_name}"
        full_name += f" {self.user.last_name}"
        return full_name

    class Meta:
        ordering = ("-created_at",)

    def clean(self):
        if self.account_type == 2 and self.citizenship_back is None:
            raise ValueError("Citizenship back image is required for owner account type")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.pk is None and self.citizenship_back is not None:
            scanned_text = scan_image_for_text(self.citizenship_back.path)
            validate_presence_of_nepal_government_text(scanned_text)
            self.citizenship_number = get_citizenship_number(scanned_text)
            scanned_full_name = get_full_name(scanned_text)
            if scanned_full_name != self.full_name:
                raise ValueError("Full name in the scanned image does not match with the full name provided")
            self.is_citizenship_verified = True
            self.save()


class ResetPasswordCode(Timestamp):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, editable=False, related_name="reset_password_codes"
    )
    code = models.UUIDField(default=uuid.uuid4, editable=False)
    is_used = models.BooleanField(default=False, editable=False)
    is_expired = models.BooleanField(default=False, editable=False)
    expired_at = models.DateTimeField(null=True, editable=False)

    class Meta:
        ordering = ("-created_at",)

    def expire(self):
        self.is_expired = True
        self.expired_at = timezone.now()
        self.save()

    def has_expired(self):
        if self.is_expired:
            return True
        if self.created_at + timezone.timedelta(minutes=RESET_PASSWORD_CODE_EXPIRE_TIME) < timezone.now():
            return True
        return False
