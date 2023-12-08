from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from review.models import Review, QAndA
from review.serializer import ReviewSerializer, QAndASerializer


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class QAndAViewSet(ModelViewSet):
    queryset = QAndA.objects.all()
    serializer_class = QAndASerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
