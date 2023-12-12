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
    GenericRelations
):
    name = models.CharField(
        max_length=255,
        blank=True,
        help_text='Descriptive name for the room (e.g., "Cozy Garden View", "Spacious Family Room").',
    )
    floor_level = models.PositiveIntegerField()
    with_kitchen_setup = models.BooleanField(default=False)
    owner_lives_in_same_building = models.BooleanField(default=True)

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
    GenericRelations
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
    GenericRelations
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

    class Meta:
        ordering = ["-created_at"]


class OfficeSpace(models.Model):
    house = models.OneToOneField(House, on_delete=models.CASCADE)
    no_of_meeting_rooms = models.PositiveIntegerField()
    no_of_desks = models.PositiveIntegerField()
    no_of_cubicles = models.PositiveIntegerField()
    on_site_kitchen = models.BooleanField(default=False)
