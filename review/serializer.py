from rest_framework.serializers import ModelSerializer, SerializerMethodField

from review.models import Review, QAndA
from util.serializer import ListMediaSerializer


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class ListReviewSerializer(ModelSerializer):
    medias = ListMediaSerializer(many=True)
    replies = SerializerMethodField()

    def get_replies(self, obj):
        return ListReviewSerializer(obj.replies.all(), many=True).data

    class Meta:
        model = Review
        exclude = ("content_type", "object_id")


class QAndASerializer(ModelSerializer):
    class Meta:
        model = QAndA
        fields = "__all__"


class ListQAndASerializer(ModelSerializer):
    medias = ListMediaSerializer(many=True)
    replies = SerializerMethodField()

    def get_replies(self, obj):
        return ListQAndASerializer(obj.replies.all(), many=True).data

    class Meta:
        model = QAndA
        exclude = ("content_type", "object_id")
