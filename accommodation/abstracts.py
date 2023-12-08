from django.db import models

from accommodation.choices import *
from accommodation.validators import validate_dimension_format, validate_nepali_phone_number


class BasicInformation(models.Model):
    description = models.TextField()
    max_occupancy = models.PositiveIntegerField()
    rent_price = models.PositiveIntegerField(help_text="Price per month in Nepali Rupees")
    availability_calendar = models.DateField()
    floor_level = models.PositiveIntegerField()
    is_booked = models.BooleanField(default=False)
    rental_type = models.IntegerField(choices=RENTAL_TYPE_CHOICES)
    square_footage = models.CharField(
        max_length=255, blank=True, help_text="Width x Length in feet", validators=[validate_dimension_format]
    )

    class Meta:
        abstract = True


class Amenities(models.Model):
    tv = models.BooleanField(default=False)
    wifi = models.BooleanField(default=False)
    air_conditioning = models.BooleanField(default=False)
    laundry = models.BooleanField(default=False)
    room_cleaning = models.BooleanField(default=False)
    parking_facility = models.IntegerField(choices=PARKING_FACILITY_CHOICES, default=4)
    available_furnishings = models.CharField(max_length=255, blank=True)

    class Meta:
        abstract = True


class Bathroom(models.Model):
    bathroom_type = models.IntegerField(choices=BATHROOM_TYPE_CHOICES)
    with_shower = models.BooleanField(default=False)
    with_bathtub = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Accessibility(models.Model):
    wheelchair_accessible = models.BooleanField(default=False)
    elevator_access = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Restrictions(models.Model):
    pets_allowed = models.BooleanField(default=False)
    smoking_allowed = models.BooleanField(default=False)
    only_couples_allowed = models.BooleanField(default=False)
    age_restriction = models.PositiveIntegerField(blank=True, null=True, help_text="Minimum age in years")

    class Meta:
        abstract = True


class Security(models.Model):
    security_guard = models.BooleanField(default=False)
    cctv = models.BooleanField(default=False)
    fire_alarm = models.BooleanField(default=False)
    fire_extinguisher = models.BooleanField(default=False)
    insurance_details = models.TextField(blank=True)

    class Meta:
        abstract = True


class Neighbourhood(models.Model):
    nearby_points_of_interest = models.TextField(blank=True)
    proximity_to_public_transport = models.CharField(max_length=255, blank=True)
    noise_level = models.IntegerField(choices=NOISE_LEVEL_CHOICES, default=4)

    class Meta:
        abstract = True


class OwnerInformation(models.Model):
    owner_full_name = models.CharField(max_length=255)
    owner_contact_number = models.CharField(max_length=10, validators=[validate_nepali_phone_number])
    my_own_asset = models.BooleanField(default=False, help_text="Check if you own the asset.")

    class Meta:
        abstract = True
