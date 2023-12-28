from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType

from account.models import Profile


class GetInstanceSerializer(serializers.Serializer):
    app_label = serializers.CharField()
    content_type = serializers.CharField()
    object_id = serializers.IntegerField()

    def get_instance(self, app_label, content_type, object_id):
        try:
            content_type = ContentType.objects.get(app_label=app_label, model=content_type)
        except ContentType.DoesNotExist:
            raise serializers.ValidationError("Invalid content type")
        model_class = content_type.model_class()
        try:
            instance = model_class.objects.get(id=object_id)
        except model_class.DoesNotExist:
            raise serializers.ValidationError("Object does not exist")
        return instance


class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = "__all__"


class BookingSerializer(GetInstanceSerializer):
    booked_by = serializers.PrimaryKeyRelatedField(
        queryset=Profile.objects.filter(is_verified=True, account_type=1)
    )
