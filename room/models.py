from django.contrib.contenttypes.fields import GenericRelation

from util.helper import validate_nepali_phone_number
from util.models import models, Location, PinStatus, ApprovalStatus, Modifiers


ROOM_TYPE_CHOICES = (
	(1, "Single"),
	(2, "Double"),
)


class Room(Modifiers, Location, ApprovalStatus, PinStatus):
	description = models.TextField()
	wifi = models.BooleanField(default=False)
	air_conditioning = models.BooleanField(default=False)
	attached_bathroom = models.BooleanField(default=False)
	max_occupancy = models.PositiveIntegerField()
	rent = models.PositiveIntegerField()
	availability_calendar = models.DateField()
	square_feet = models.FloatField()
	with_kitchen_setup = models.BooleanField(default=False)
	parking_facility = models.BooleanField(default=False)
	nearby_points_of_interest = models.TextField(blank=True)
	is_booked = models.BooleanField(default=False)
	type = models.IntegerField(blank=True, choices=ROOM_TYPE_CHOICES, default=1)
	available_furnishing = models.CharField(max_length=255, blank=True)
	medias = GenericRelation("util.Media", related_query_name="room")
	reviews = GenericRelation("review.Review", related_query_name="review")
	qnas = GenericRelation("review.QAndA", related_query_name="qna")
	proximity_to_public_transport = models.CharField(max_length=255, blank=True)
	owner_contact_number = models.CharField(max_length=10, validators=[validate_nepali_phone_number])
	floor = models.PositiveIntegerField()

	class Meta:
		verbose_name_plural = "Rooms"
		ordering = ["-created_at"]
		unique_together = [
			["latitude", "longitude"],
			["owner_contact_number", "floor"],
		]
