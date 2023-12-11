from django.contrib.contenttypes.fields import GenericRelation

from accommodation.abstracts import *
from media.models import Location, PinStatus, ApprovalStatus, Modifiers


class Room(
    BasicInformation,
    Amenities,
    Bathroom,
    Accessibility,
    Restrictions,
    Security,
    Neighbourhood,
    OwnerInformation,
    Modifiers,
    Location,
    ApprovalStatus,
    PinStatus,
):
    name = models.CharField(
        max_length=255,
        blank=True,
        help_text='Descriptive name for the room (e.g., "Cozy Garden View", "Spacious Family Room").',
    )
    with_kitchen_setup = models.BooleanField(default=False)
    owner_lives_in_same_building = models.BooleanField(default=True)

    # relations
    medias = GenericRelation("util.Media", related_query_name="room")
    reviews = GenericRelation("review.Review", related_query_name="room")
    qnas = GenericRelation("review.QAndA", related_query_name="room")

    class Meta:
        verbose_name_plural = "Rooms"
        ordering = ["-created_at"]


class Flat(
    BasicInformation,
    Amenities,
    Bathroom,
    Accessibility,
    Restrictions,
    Security,
    Neighbourhood,
    OwnerInformation,
    Modifiers,
    Location,
    ApprovalStatus,
    PinStatus,
):
    name = models.CharField(
        max_length=255,
        blank=True,
        help_text='Descriptive name for the flat (e.g., "Modern Studio in Trendy Neighborhood", "Spacious Family '
        'Flat with Balcony"). ',
    )
    no_of_bedrooms = models.PositiveIntegerField()
    no_of_bathrooms = models.PositiveIntegerField()
    with_kitchen = models.BooleanField(default=True)

    building_type = models.IntegerField(choices=BUILDING_TYPE_CHOICES)
    year_built = models.IntegerField()
    is_furnished = models.BooleanField(default=False)
    security_deposit = models.PositiveIntegerField(blank=True, null=True)

    # relations
    medias = GenericRelation("util.Media", related_query_name="flat")
    reviews = GenericRelation("review.Review", related_query_name="flat")
    qnas = GenericRelation("review.QAndA", related_query_name="flat")

    class Meta:
        verbose_name_plural = "Flats"
        ordering = ["-created_at"]
