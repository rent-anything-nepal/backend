from rest_framework.serializers import ModelSerializer, SerializerMethodField

from accommodation.models import Room, Flat
from util.serializer import ListMediaSerializer
from review.serializer import ListReviewSerializer, ListQAndASerializer


class RoomSerializer(ModelSerializer):
    medias = ListMediaSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = "__all__"


class RoomDetailSerializer(ModelSerializer):
    medias = ListMediaSerializer(many=True, read_only=True)
    reviews = SerializerMethodField()
    qnas = SerializerMethodField()

    def get_reviews(self, obj):
        return ListReviewSerializer(obj.reviews.filter(reply_to=None), many=True).data

    def get_qnas(self, obj):
        return ListQAndASerializer(obj.qnas.filter(reply_to=None), many=True).data

    class Meta:
        model = Room
        fields = "__all__"


class FlatSerializer(ModelSerializer):
    medias = ListMediaSerializer(many=True, read_only=True)

    class Meta:
        model = Flat
        fields = "__all__"


class FlatDetailSerializer(ModelSerializer):
    medias = ListMediaSerializer(many=True, read_only=True)
    reviews = SerializerMethodField()
    qnas = SerializerMethodField()

    def get_reviews(self, obj):
        return ListReviewSerializer(obj.reviews.filter(reply_to=None), many=True).data

    def get_qnas(self, obj):
        return ListQAndASerializer(obj.qnas.filter(reply_to=None), many=True).data

    class Meta:
        model = Flat
        fields = "__all__"
