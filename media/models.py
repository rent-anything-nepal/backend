from uuid import uuid4

from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.contrib.contenttypes.models import ContentType

from media.validators import validate_file_extension, validate_file_size
from utils.abstracts import Modifiers
from utils.helpers import check_if_object_id_exists


def get_media_upload_to_path(instance, filename):
    ext = filename.split(".")[-1]
    return f"media/{instance.content_type}/{instance.object_id}/{uuid4()}.{ext}"


class Media(Modifiers):
    media = models.FileField(
        upload_to=get_media_upload_to_path,
        validators=[validate_file_extension, validate_file_size],
    )
    caption = models.CharField(max_length=255, blank=True)
    alt_text = models.CharField(max_length=255, blank=True)

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="media",
        limit_choices_to={"model__in": ("room", "flat", "house", "review", "qanda")},
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        ordering = ["-created_at"]

    def clean(self) -> None:
        check_if_object_id_exists(self)
