from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError

from review.models import Review, QAndA
from media.serializer import ListMediaSerializer


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"

    def validate(self, data):
        instance = Review(**data)
        instance.clean()
        return data


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

    def validate(self, data):
        instance = QAndA(**data)
        instance.clean()
        return data


class ListQAndASerializer(ModelSerializer):
    medias = ListMediaSerializer(many=True)
    replies = SerializerMethodField()

    def get_replies(self, obj):
        return ListQAndASerializer(obj.replies.all(), many=True).data

    class Meta:
        model = QAndA
        exclude = ("content_type", "object_id")
