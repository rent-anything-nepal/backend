from rest_framework.serializers import ModelSerializer, SerializerMethodField

from accommodation.filters import EXCLUDED_FIELDS_FOR_PUBLIC
from accommodation.models import Room, Flat, House
from media.serializer import ListMediaSerializer
from review.serializer import ListReviewSerializer, ListQAndASerializer


class BaseCompleteSerializer(ModelSerializer):
    medias = ListMediaSerializer(many=True, read_only=True)
    reviews = SerializerMethodField()
    qnas = SerializerMethodField()

    def get_reviews(self, obj):
        return ListReviewSerializer(obj.reviews.filter(reply_to=None), many=True).data

    def get_qnas(self, obj):
        return ListQAndASerializer(obj.qnas.filter(reply_to=None), many=True).data

    class Meta:
        abstract = True


class BaseOnlyMediaSerializer(ModelSerializer):
    medias = ListMediaSerializer(many=True, read_only=True)

    class Meta:
        abstract = True


class PublicRoomDetailSerializer(BaseCompleteSerializer):
    class Meta:
        model = Room
        exclude = EXCLUDED_FIELDS_FOR_PUBLIC


class PublicRoomListSerializer(BaseOnlyMediaSerializer):
    class Meta:
        model = Room
        exclude = EXCLUDED_FIELDS_FOR_PUBLIC


class AdminRoomListSerializer(BaseOnlyMediaSerializer):
    class Meta:
        model = Room
        fields = "__all__"


class AdminRoomDetailSerializer(BaseCompleteSerializer):
    class Meta:
        model = Room
        fields = "__all__"


class AdminFlatListSerializer(BaseOnlyMediaSerializer):
    class Meta:
        model = Flat
        fields = "__all__"


class AdminFlatDetailSerializer(BaseCompleteSerializer):
    class Meta:
        model = Flat
        fields = "__all__"


class PublicFlatDetailSerializer(BaseCompleteSerializer):
    class Meta:
        model = Flat
        exclude = EXCLUDED_FIELDS_FOR_PUBLIC


class PublicFlatListSerializer(BaseOnlyMediaSerializer):
    class Meta:
        model = Flat
        exclude = EXCLUDED_FIELDS_FOR_PUBLIC


class PublicHouseDetailSerializer(BaseCompleteSerializer):
    class Meta:
        model = House
        exclude = EXCLUDED_FIELDS_FOR_PUBLIC


class PublicHouseListSerializer(BaseOnlyMediaSerializer):
    class Meta:
        model = House
        exclude = EXCLUDED_FIELDS_FOR_PUBLIC


class AdminHouseListSerializer(BaseOnlyMediaSerializer):
    class Meta:
        model = House
        fields = "__all__"


class AdminHouseDetailSerializer(BaseCompleteSerializer):
    class Meta:
        model = House
        fields = "__all__"
