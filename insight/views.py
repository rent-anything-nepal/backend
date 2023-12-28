from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from insight.models import Review, QAndA, Rule, SavedSearch
from insight.serializer import (
    ReviewSerializer,
    QAndASerializer,
    ListReviewSerializer,
    ListQAndASerializer,
    RuleSerializer, SavedSearchSerializer,
)
from utils.abstracts import BaseViewSet


class ReviewFilter(filters.FilterSet):
    rating = filters.RangeFilter()

    class Meta:
        model = Review
        fields = ["post_anonymously", "reply_to", "object_id", "content_type"]


class ReviewViewSet(BaseViewSet):
    queryset = Review.objects.filter(reply_to__isnull=True)
    search_fields = ["comment"]
    filterset_class = ReviewFilter

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return ReviewSerializer
        return ListReviewSerializer


class QAndAViewSet(BaseViewSet):
    queryset = QAndA.objects.filter(reply_to__isnull=True)
    search_fields = ["comment"]
    filterset_fields = ["object_id", "content_type", "post_anonymously"]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return QAndASerializer
        return ListQAndASerializer


class RuleViewSet(BaseViewSet):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer
    search_fields = ["content"]
    filterset_fields = ["object_id", "content_type"]


class SavedSearchView(APIView):
    def post(self, request):
        serializer = SavedSearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            ip_address=self.request.META.get("HTTP_X_FORWARDED_FOR", self.request.META.get("REMOTE_ADDR"))
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        saved_searches = SavedSearch.objects.filter(
            ip_address=self.request.META.get("HTTP_X_FORWARDED_FOR", self.request.META.get("REMOTE_ADDR"))
        )
        serializer = SavedSearchSerializer(saved_searches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
