from django.contrib.contenttypes.fields import GenericRelation

from accommodation.abstracts import *
from accommodation.validators import validate_created_by
from utils.abstracts import Location, PinStatus, ApprovalStatus, Modifiers


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
    floor_level = models.PositiveIntegerField()
    with_kitchen_setup = models.BooleanField(default=False)
    owner_lives_in_same_building = models.BooleanField(default=True)

    # relations
    medias = GenericRelation("media.Media", related_query_name="room")
    reviews = GenericRelation("review.Review", related_query_name="room")
    qnas = GenericRelation("review.QAndA", related_query_name="room")

    class Meta:
        ordering = ["-created_at"]

    def clean(self) -> None:
        validate_created_by(self)


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
    FlatAttributes,
):
    name = models.CharField(
        max_length=255,
        blank=True,
        help_text='Descriptive name for the flat (e.g., "Modern Studio in Trendy Neighborhood", "Spacious Family '
        'Flat with Balcony").',
    )
    floor_level = models.PositiveIntegerField()
    with_kitchen = models.BooleanField(default=True)
    owner_lives_in_same_building = models.BooleanField(default=True)
    for_office_use_only = models.BooleanField(default=False)

    # relations
    medias = GenericRelation("media.Media", related_query_name="flat")
    reviews = GenericRelation("review.Review", related_query_name="flat")
    qnas = GenericRelation("review.QAndA", related_query_name="flat")

    class Meta:
        ordering = ["-created_at"]

    def clean(self) -> None:
        validate_created_by(self)


class House(
    BasicInformation,
    Accessibility,
    Restrictions,
    Security,
    Neighbourhood,
    OwnerInformation,
    Modifiers,
    Location,
    ApprovalStatus,
    PinStatus,
    FlatAttributes,
    SmartFeatures,
    HouseAmenities,
):
    name = models.CharField(
        max_length=255,
        blank=True,
        help_text='Descriptive name for the house (e.g., "Charming Cottage with Garden", "Modern Family Home").',
    )

    no_of_floors = models.PositiveIntegerField()
    for_office_use_only = models.BooleanField(default=False)
    with_customizable_option = models.BooleanField(default=False)
    post_move_in_support = models.BooleanField(default=False)

    # relations
    medias = GenericRelation("media.Media", related_query_name="house")
    reviews = GenericRelation("review.Review", related_query_name="house")
    qnas = GenericRelation("review.QAndA", related_query_name="house")

    class Meta:
        ordering = ["-created_at"]


class OfficeSpace(models.Model):
    house = models.OneToOneField(House, on_delete=models.CASCADE)
    no_of_meeting_rooms = models.PositiveIntegerField()
    no_of_desks = models.PositiveIntegerField()
    no_of_cubicles = models.PositiveIntegerField()
    on_site_kitchen = models.BooleanField(default=False)
