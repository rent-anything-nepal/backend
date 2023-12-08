from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from room.models import Room
from room.serializer import RoomSerializer, RoomDetailSerializer

ROOM_FILTERS = [
	"wifi",
	"air_conditioning",
	"attached_bathroom",
	"max_occupancy",
	"rent",
	"with_kitchen_setup",
	"parking_facility",
	"is_booked",
	"type",
]

ROOM_SEARCH_FIELDS = [
	"description",
	"nearby_points_of_interest",
	"available_furnishing",
	"proximity_to_public_transport",
]


class RoomViewSet(viewsets.ModelViewSet):
	queryset = Room.objects.all()
	permission_classes = [IsAuthenticated]
	filterset_fields = ROOM_FILTERS
	search_fields = ROOM_SEARCH_FIELDS

	def get_serializer_class(self):
		if self.action == "retrieve":
			return RoomDetailSerializer
		return RoomSerializer

	def perform_create(self, serializer):
		serializer.save(created_by=self.request.user)

	def perform_update(self, serializer):
		serializer.save(updated_by=self.request.user)


class RoomPublicViewSet(viewsets.ReadOnlyModelViewSet):
	serializer_class = RoomSerializer
	filterset_fields = ROOM_FILTERS
	search_fields = ROOM_SEARCH_FIELDS

	def get_queryset(self):
		return Room.objects.filter(
			is_booked=False,
			approval_status=True,
		)
