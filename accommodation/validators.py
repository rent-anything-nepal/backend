from re import match as re_match
from django.core.exceptions import ValidationError


def validate_dimension_format(value):
    """
    Validates the format of the dimension field.
    """
    if not re_match(r"^\d+\s*x\s*\d+$", value):
        raise ValidationError("Dimension format should be in the form of 'Width x Length'")


def validate_nepali_phone_number(value):
    regex_mobile = r"^(98[0-9]{8})$"
    regex_landline = r"^(0[1-9]{1}[0-9]{7})$"

    if not re_match(regex_mobile, value) and not re_match(regex_landline, value):
        raise ValidationError("Invalid phone number.")


def validate_created_by(instance):
    self = instance
    if self.created_by.profile.account_type == 1:
        raise ValidationError("You need to be an owner or a maintainer to add a room.")
    if not self.my_own_asset and (self.owner_full_name is None or self.owner_contact_number is None):
        raise ValidationError("Owner's full name and contact number are required if you don't own the asset.")
    if self.my_own_asset and self.created_by.profile.is_profile_verified is False:
        raise ValidationError("You need to verify your profile before adding your own asset.")
