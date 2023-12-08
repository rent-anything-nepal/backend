from uuid import uuid4
from os.path import splitext
from django.core.exceptions import ValidationError

VALID_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png"]
VALID_VIDEO_EXTENSIONS = [".mp4"]


def get_media_upload_to_path(instance, filename):
    ext = filename.split(".")[-1]
    random_filename = f"{uuid4()}.{ext}"
    return f"media/{instance.content_type}/{instance.object_id}/{random_filename}"


def validate_file_extension(value):
    ext = splitext(value.name)[1]
    valid_extensions = VALID_IMAGE_EXTENSIONS + VALID_VIDEO_EXTENSIONS
    if not ext.lower() in valid_extensions:
        raise ValidationError(
            "Unsupported file extension. Supported extensions are: " + ", ".join(valid_extensions)
        )


def validate_file_size(value):
    from os.path import splitext

    ext = splitext(value.name)[1]
    if ext.lower() in VALID_IMAGE_EXTENSIONS and value.size > 10485760:
        raise ValidationError("Image size should not be greater than 10MB.")
    elif ext.lower() in VALID_VIDEO_EXTENSIONS and value.size > 104857600:
        raise ValidationError("Video size should not be greater than 100MB.")
