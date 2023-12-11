import re

from django.core.exceptions import ValidationError


def validate_citizenship_number(value):
    regex = r"^(?:\d+\-){2,3}\d+$"
    if not re.match(regex, value):
        raise ValidationError(
            _("%(value)s is not a valid citizenship number"),
            params={"value": value},
        )
