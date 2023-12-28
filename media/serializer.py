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

    def validate(self, data):
        instance = Media(**data)
        instance.clean()
        return data
