from django_filters import rest_framework as filters
from insight.models import Review, QAndA, Rule
from insight.serializer import ReviewSerializer, QAndASerializer, ListReviewSerializer, ListQAndASerializer, \
    RuleSerializer
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
