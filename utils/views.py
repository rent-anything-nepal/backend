from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_condition import And, Or

from account.permissions import IsSuperUser
from utils.permissions import IsMyProperty
from utils.serializers import GetInstanceSerializer, ContentTypeSerializer, ContentType, BookingSerializer


class BaseActionView(APIView):
    permission_classes = [And(IsAuthenticated, IsSuperUser)]

    def perform_post_action(self, request, instance):
        raise NotImplementedError

    def perform_delete_action(self, instance):
        raise NotImplementedError

    def post(self, request, *args, **kwargs):
        serializer = GetInstanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.get_instance(**serializer.validated_data)
        self.perform_post_action(request, instance)
        return Response(status=200)

    def delete(self, request, *args, **kwargs):
        serializer = GetInstanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.get_instance(**serializer.validated_data)
        self.perform_delete_action(request, instance)
        return Response(status=200)


class ApprovalView(BaseActionView):
    def perform_post_action(self, request, instance):
        if not instance.is_approved:
            instance.is_approved = True
            instance.approved_at = timezone.now()
            instance.approved_by = request.user
            instance.save()

    def perform_delete_action(self, instance):
        if instance.is_approved:
            instance.is_approved = False
            instance.approved_at = None
            instance.approved_by = None
            instance.save()


class PinView(BaseActionView):
    permission_classes = [And(IsAuthenticated, IsSuperUser)]

    def perform_post_action(self, request, instance):
        if not instance.is_pinned:
            instance.is_pinned = True
            instance.pinned_at = timezone.now()
            instance.pinned_by = request.user
            instance.save()

    def perform_delete_action(self, instance):
        if instance.is_pinned:
            instance.is_pinned = False
            instance.pinned_at = None
            instance.pinned_by = None
            instance.save()


class ContentTypesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content_types = ContentType.objects.all()
        serializer = ContentTypeSerializer(content_types, many=True)
        return Response(serializer.data)


class BookingView(APIView):
    permission_classes = [And(IsAuthenticated, Or(IsSuperUser, IsMyProperty))]

    def post(self, request, *args, **kwargs):
        serializer = BookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.get_instance(**serializer.validated_data)
        if instance.is_booked:
            return Response({"detail": "Already booked"}, status=400)
        instance.is_booked = True
        instance.booked_by = serializer.validated_data.get("booked_by")
        instance.booked_at = timezone.now()
        instance.save()
        return Response(status=200)

    def delete(self, request, *args, **kwargs):
        serializer = GetInstanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.get_instance(**serializer.validated_data)
        if not instance.is_booked:
            return Response({"detail": "Not booked"}, status=400)
        instance.is_booked = False
        instance.booked_by = None
        instance.booked_at = None
        instance.save()
        return Response(status=200)
