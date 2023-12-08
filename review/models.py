from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

from review.validators import divisible_by_point_five
from util.models import Modifiers, models, ContentType
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(Modifiers):
	rating = models.FloatField(
		null=True, help_text="Rating should be between 0.0 and 5.0",
		validators=[MinValueValidator(0.0), MaxValueValidator(5.0), divisible_by_point_five]
	)
	comment = models.TextField()
	post_anonymously = models.BooleanField(default=False)

	object_id = models.PositiveIntegerField()
	content_type = models.ForeignKey(
		ContentType, on_delete=models.CASCADE, related_name="reviews",
		limit_choices_to={'model__in': ('room',)}
	)
	content_object = GenericForeignKey("content_type", "object_id")
	medias = GenericRelation("util.Media", related_query_name="review")

	reply_to = models.ForeignKey(
		"self", on_delete=models.CASCADE, null=True, related_name="replies"
	)

	class Meta:
		unique_together = [
			["created_by", "object_id", "content_type"],
		]
		ordering = ["-created_at"]
		verbose_name_plural = "Reviews"


class QAndA(Modifiers):
	comment = models.TextField()
	post_anonymously = models.BooleanField(default=False)

	object_id = models.PositiveIntegerField()
	content_type = models.ForeignKey(
		ContentType, on_delete=models.CASCADE, related_name="qnas",
		limit_choices_to={'model__in': ('room',)}
	)
	content_object = GenericForeignKey("content_type", "object_id")
	medias = GenericRelation("util.Media", related_query_name="qna")

	reply_to = models.ForeignKey(
		"self", on_delete=models.CASCADE, null=True, related_name="replies"
	)

	class Meta:
		ordering = ["-created_at"]
		verbose_name = "Q&A"
		verbose_name_plural = "Q&As"
