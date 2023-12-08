from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.contrib.contenttypes.models import ContentType

from util.helper import get_media_upload_to_path, validate_file_extension, validate_file_size


class Timestamp(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class Modifiers(models.Model):
	created_by = models.ForeignKey(
		get_user_model(), on_delete=models.CASCADE, related_name="created_%(class)s", editable=False
	)
	updated_by = models.ForeignKey(
		get_user_model(),
		on_delete=models.CASCADE,
		null=True,
		related_name="updated_%(class)s",
		editable=False,
	)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class ApprovalStatus(models.Model):
	is_approved = models.BooleanField(default=False, editable=False)
	approved_by = models.ForeignKey(
		get_user_model(),
		on_delete=models.CASCADE,
		null=True,
		related_name="approved_%(class)s",
		editable=False,
	)
	approved_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		abstract = True


class PinStatus(models.Model):
	is_pinned = models.BooleanField(default=False, editable=False)
	pinned_by = models.ForeignKey(
		get_user_model(), on_delete=models.CASCADE, null=True, related_name="pinned_%(class)s", editable=False
	)
	pinned_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		abstract = True


class Location(models.Model):
	latitude = models.FloatField()
	longitude = models.FloatField()
	address = models.CharField(max_length=255)
	city = models.CharField(max_length=255)
	province = models.CharField(max_length=255)

	class Meta:
		abstract = True


class Media(Modifiers):
	media = models.FileField(
		upload_to=get_media_upload_to_path,
		validators=[validate_file_extension, validate_file_size],
	)
	caption = models.CharField(max_length=255, blank=True)
	alt_text = models.CharField(max_length=255, blank=True)

	content_type = models.ForeignKey(
		ContentType, on_delete=models.CASCADE, related_name="media",
		limit_choices_to={'model__in': ('room', 'review', 'qanda')}
	)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey("content_type", "object_id")

	class Meta:
		ordering = ["-created_at"]
		verbose_name_plural = "Medias"
