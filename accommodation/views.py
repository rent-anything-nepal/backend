from rest_condition import And, Or
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Count

from accommodation.filters import *
from accommodation.models import Room, Flat, House
from accommodation.serializer import (
    PublicRoomDetailSerializer,
    PublicRoomListSerializer,
    AdminRoomDetailSerializer,
    AdminRoomListSerializer,
    PublicFlatDetailSerializer,
    PublicFlatListSerializer,
    AdminFlatDetailSerializer,
    AdminFlatListSerializer,
)
from account.permissions import IsSuperUser
from utils.permissions import IsMyProperty


class BaseAdminViewSet(viewsets.ModelViewSet):
    search_fields = COMMON_SEARCH_FIELDS

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy", "retrieve"]:
            permission_classes = [And(IsAuthenticated, Or(IsSuperUser, IsMyProperty))]
        else:
            permission_classes = [And(IsAuthenticated, IsSuperUser)]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    class Meta:
        abstract = True


class PublicRoomViewSet(viewsets.ReadOnlyModelViewSet):
    filterset_class = RoomFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PublicRoomDetailSerializer
        return PublicRoomListSerializer

    def get_queryset(self):
        return Room.object.annotate(
            accepted_booking_requests=Count(
                "booking_requests",
                filter=Q(booking_request__is_accepted=True),
            )
        ).filter(accepted_booking_requests=0, is_approved=True)


class AdminRoomViewSet(BaseAdminViewSet):
    queryset = Room.objects.all()
    filterset_class = RoomAdminFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AdminRoomDetailSerializer
        return AdminRoomListSerializer


class PublicFlatViewSet(viewsets.ReadOnlyModelViewSet):
    filterset_class = FlatFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PublicFlatDetailSerializer
        return PublicFlatListSerializer

    def get_queryset(self):
        return Flat.objects.filter(
            is_booked=False,
            approval_status=True,
        )


class AdminFlatViewSet(BaseAdminViewSet):
    queryset = Flat.objects.all()
    filterset_class = FlatAdminFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AdminFlatDetailSerializer
        return AdminFlatListSerializer


class PublicHouseViewSet(viewsets.ReadOnlyModelViewSet):
    filterset_class = HouseFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PublicFlatDetailSerializer
        return PublicFlatListSerializer

    def get_queryset(self):
        return House.objects.filter(
            is_booked=False,
            approval_status=True,
        )


class AdminHouseViewSet(BaseAdminViewSet):
    queryset = House.objects.all()
    filterset_class = HouseAdminFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AdminFlatDetailSerializer
        return AdminFlatListSerializer
