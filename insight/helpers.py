from django.core.exceptions import ValidationError


def divisible_by_point_five(value):
    if value % 0.5 != 0:
        raise ValidationError("Rating should be divisible by 0.5")
