from django.db import models

from accommodation.choices import *
from accommodation.validators import validate_dimension_format, validate_nepali_phone_number


class BasicInformation(models.Model):
    description = models.TextField()
    max_occupancy = models.PositiveIntegerField()
    rent_price = models.PositiveIntegerField(help_text="Price per month in Nepali Rupees")
    availability_calendar = models.DateField()
    is_booked = models.BooleanField(default=False)
    rental_type = models.IntegerField(choices=RENTAL_TYPE_CHOICES)
    square_footage = models.CharField(
        max_length=255, blank=True, help_text="Width x Length in feet", validators=[validate_dimension_format]
    )
    natural_light = models.IntegerField(choices=NATURAL_LIGHT_CHOICES, default=1)
    security_deposit = models.PositiveIntegerField(default=0)
    is_negotiable = models.BooleanField(default=False)
    water_supply = models.IntegerField(choices=WATER_SUPPLY_CHOICES, default=1)
    minimum_stay = models.IntegerField(choices=MINIMUM_STAY_CHOICES, default=1)
    is_furnished = models.BooleanField(default=False)
    available_furnishings = models.CharField(max_length=512, blank=True)

    class Meta:
        abstract = True


class Amenities(models.Model):
    tv = models.BooleanField(default=False)
    internet = models.BooleanField(default=False)
    air_conditioning = models.BooleanField(default=False)
    laundry = models.BooleanField(default=False)
    room_cleaning = models.BooleanField(default=False)
    parking_facility = models.IntegerField(choices=PARKING_FACILITY_CHOICES, default=4)
    electricity_backup = models.BooleanField(default=False)

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
    view_from_accommodation = models.TextField(blank=True)
    nearby_points_of_interest = models.TextField(blank=True)
    proximity_to_public_transport = models.CharField(max_length=255, blank=True)
    noise_level = models.IntegerField(choices=NOISE_LEVEL_CHOICES, default=4)

    class Meta:
        abstract = True


class OwnerInformation(models.Model):
    owner_full_name = models.CharField(max_length=255, null=True)
    owner_contact_number = models.CharField(
        max_length=10, validators=[validate_nepali_phone_number], null=True
    )
    my_own_asset = models.BooleanField(default=False, help_text="Check if you own the asset.")

    class Meta:
        abstract = True


class SmartFeatures(models.Model):
    smart_tv = models.BooleanField(default=False)
    smart_lighting = models.BooleanField(default=False)
    smart_lock = models.BooleanField(default=False)
    smart_thermostat = models.BooleanField(default=False)
    smart_speaker = models.BooleanField(default=False)
    smart_plug = models.BooleanField(default=False)
    smart_camera = models.BooleanField(default=False)
    smart_doorbell = models.BooleanField(default=False)

    class Meta:
        abstract = True


class FlatAttributes(models.Model):
    no_of_bedrooms = models.PositiveIntegerField()
    no_of_bathrooms = models.PositiveIntegerField()
    building_type = models.IntegerField(choices=BUILDING_TYPE_CHOICES)
    year_built = models.IntegerField()

    class Meta:
        abstract = True


class HouseAmenities(models.Model):
    with_garden = models.BooleanField(default=False)
    with_balcony = models.BooleanField(default=False)
    with_terrace = models.BooleanField(default=False)
    with_rooftop_deck = models.BooleanField(default=False)
    with_pool = models.BooleanField(default=False)
    with_gym = models.BooleanField(default=False)
    with_fireplace = models.BooleanField(default=False)

    class Meta:
        abstract = True
