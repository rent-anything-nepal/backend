from django.contrib.contenttypes.models import ContentType
from rest_framework.serializers import ModelSerializer

from media.models import Media


class ListMediaSerializer(ModelSerializer):
    class Meta:
        model = Media
        fields = ("id", "media")


class MediaSerializer(ModelSerializer):
    class Meta:
        model = Media
        fields = "__all__"


class ContentTypeSerializer(ModelSerializer):
    class Meta:
        model = ContentType
        fields = ("id", "name")
