from django_filters import rest_framework as filters

from accommodation.models import Room, Flat, House

EXCLUDED_FIELDS_FOR_PUBLIC = (
    "is_booked",
    "is_approved",
    "approved_by",
    "approved_at",
    "pinned_by",
    "pinned_at",
    "is_pinned",
)

COMMON_FILTERS = [
    "rental_type",
    "natural_light",
    "is_negotiable",
    "water_supply",
    "minimum_stay",
    "wheelchair_accessible",
    "elevator_access",
    "no_smoking",
    "only_family",
    "security_guard",
    "cctv",
    "fire_alarm",
    "fire_extinguisher",
    "noise_level",
    "ward",
    "ward__municipality",
    "ward__municipality__district",
    "ward__municipality__district__province",
]
AMENITIES_FILTERS = [
    "tv",
    "internet",
    "air_conditioning",
    "laundry",
    "room_cleaning",
    "parking_facility",
    "electricity_backup",
]
BATHROOM_FILTERS = [
    "bathroom_type",
    "with_shower",
    "with_bathtub",
]
ROOM_FILTERS = (
    [
        "floor_level",
        "with_kitchen_setup",
        "owner_lives_in_same_building",
    ]
    + COMMON_FILTERS
    + AMENITIES_FILTERS
    + BATHROOM_FILTERS
)
FLAT_FILTERS = (
    [
        "floor_level",
        "with_kitchen",
        "owner_lives_in_same_building",
        "building_type",
        "for_office_use_only",
    ]
    + COMMON_FILTERS
    + AMENITIES_FILTERS
    + BATHROOM_FILTERS
)
HOUSE_FILTERS = [
    "no_of_floors",
    "for_office_use_only",
    "with_customizable_option",
    "post_move_in_support",
    "building_type",
    "with_garden",
    "with_balcony",
    "with_terrace",
    "with_rooftop_deck",
    "with_pool",
    "with_gym",
    "with_fireplace",
    "for_office_use_only",
] + COMMON_FILTERS

ADMIN_FILTERS = [
    "is_approved",
    "is_pinned",
    "my_own_asset",
]

COMMON_SEARCH_FIELDS = [
    "name",
    "description",
    "square_footage",
    "available_furnishings",
    "insurance_details",
    "view_from_accommodation",
    "nearby_points_of_interest",
    "proximity_to_public_transport",
    "owner_full_name",
    "owner_contact_number",
    "address",
    "created_by__username",
    "created_by__first_name",
    "created_by__last_name",
]


class AccommodationBaseFilter(filters.FilterSet):
    rent_price = filters.RangeFilter()
    security_deposit = filters.RangeFilter()
    # availability_calendar = filters.DateFromToRangeFilter()


class RoomAdminFilter(AccommodationBaseFilter):
    class Meta:
        model = Room
        fields = ROOM_FILTERS + ADMIN_FILTERS


class RoomFilter(AccommodationBaseFilter):
    class Meta:
        model = Room
        fields = ROOM_FILTERS


class FlatAdminFilter(AccommodationBaseFilter):
    class Meta:
        model = Flat
        fields = FLAT_FILTERS + ADMIN_FILTERS


class FlatFilter(AccommodationBaseFilter):
    class Meta:
        model = Flat
        fields = FLAT_FILTERS


class HouseAdminFilter(AccommodationBaseFilter):
    class Meta:
        model = House
        fields = HOUSE_FILTERS + ADMIN_FILTERS


class HouseFilter(AccommodationBaseFilter):
    class Meta:
        model = House
        fields = HOUSE_FILTERS
