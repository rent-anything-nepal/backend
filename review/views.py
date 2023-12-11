from review.models import Review, QAndA
from review.serializer import ReviewSerializer, QAndASerializer, ListReviewSerializer, ListQAndASerializer
from utils.abstracts import BaseViewSet


class ReviewViewSet(BaseViewSet):
    queryset = Review.objects.filter(reply_to__isnull=True)

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return ReviewSerializer
        return ListReviewSerializer


class QAndAViewSet(BaseViewSet):
    queryset = QAndA.objects.filter(reply_to__isnull=True)

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return QAndASerializer
        return ListQAndASerializer
