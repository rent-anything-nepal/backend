from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from accommodation.filters import ROOM_FILTERS, ROOM_SEARCH_FIELDS
from accommodation.models import Room, Flat
from accommodation.serializer import RoomSerializer, RoomDetailSerializer, FlatSerializer, FlatDetailSerializer


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


class FlatViewSet(viewsets.ModelViewSet):
    queryset = Flat.objects.all()
    permission_classes = [IsAuthenticated]
    filterset_fields = ROOM_FILTERS
    search_fields = ROOM_SEARCH_FIELDS

    def get_serializer_class(self):
        if self.action == "retrieve":
            return FlatDetailSerializer
        return FlatSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class FlatPublicViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FlatSerializer
    filterset_fields = ROOM_FILTERS
    search_fields = ROOM_SEARCH_FIELDS

    def get_queryset(self):
        return Flat.objects.filter(
            is_booked=False,
            approval_status=True,
        )
