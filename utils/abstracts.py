from django.db import models
from django.contrib.auth import get_user_model
from rest_condition import And, Or
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from account.permissions import IsSuperUser
from utils.permissions import IsMyProperty


class Timestamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Modifiers(models.Model):
    created_by = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="created_%(class)s", editable=False
    )
    updated_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True,
        related_name="updated_%(class)s",
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ApprovalStatus(models.Model):
    is_approved = models.BooleanField(default=False, editable=False)
    approved_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True,
        related_name="approved_%(class)s",
        editable=False,
    )
    approved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class PinStatus(models.Model):
    is_pinned = models.BooleanField(default=False, editable=False)
    pinned_by = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, null=True, related_name="pinned_%(class)s", editable=False
    )
    pinned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=255)

    ward = models.ForeignKey("location.Ward", on_delete=models.CASCADE)

    class Meta:
        abstract = True


class BaseViewSet(ModelViewSet):
    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy", "list", "retrieve"]:
            permission_classes = [And(IsAuthenticated, Or(IsSuperUser, IsMyProperty))]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    class Meta:
        abstract = True
