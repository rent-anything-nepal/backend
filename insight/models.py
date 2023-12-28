from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.auth import get_user_model

from accommodation.validators import validate_only_future_dates
from insight.helpers import divisible_by_point_five
from media.models import Modifiers, models, ContentType
from django.core.validators import MinValueValidator, MaxValueValidator

from utils.helpers import check_if_object_id_exists


class BaseGenericKey(models.Model):
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="%(class)s",
        limit_choices_to={"model__in": ("room", "flat", "house")},
    )
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        abstract = True


class Review(Modifiers, BaseGenericKey):
    comment = models.TextField()
    post_anonymously = models.BooleanField(default=False)
    medias = GenericRelation("media.Media", related_query_name="review")
    rating = models.FloatField(
        null=True,
        help_text="Rating should be between 0.0 and 5.0",
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0), divisible_by_point_five],
    )
    reply_to = models.ForeignKey("self", on_delete=models.CASCADE, null=True, related_name="replies")

    class Meta:
        unique_together = [
            ["created_by", "object_id", "content_type"],
        ]
        ordering = ["-created_at"]

    def clean(self) -> None:
        check_if_object_id_exists(self)


class QAndA(Modifiers, BaseGenericKey):
    comment = models.TextField()
    post_anonymously = models.BooleanField(default=False)
    medias = GenericRelation("media.Media", related_query_name="qna")
    reply_to = models.ForeignKey("self", on_delete=models.CASCADE, null=True, related_name="replies")

    class Meta:
        ordering = ["-created_at"]

    def clean(self) -> None:
        check_if_object_id_exists(self)


class Rule(Modifiers, BaseGenericKey):
    title = models.CharField(max_length=255, unique=True)
    content = models.TextField()

    def clean(self) -> None:
        check_if_object_id_exists(self)

    class Meta:
        ordering = ["-created_at"]
        unique_together = [["content", "object_id", "content_type"]]


class BookingRequest(Modifiers, BaseGenericKey):
    start_date = models.DateField(validators=[validate_only_future_dates])
    rent_price = models.FloatField()
    message = models.TextField(null=True)
    start_date_range_to = models.DateField(null=True, validators=[validate_only_future_dates])

    is_accepted = models.BooleanField(default=False)
    accepted_at = models.DateTimeField(null=True, editable=False)
    accepted_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        editable=False,
        related_name="%(class)s_acceptances",
    )

    class Meta:
        ordering = ["-created_at"]
        unique_together = [
            ["object_id", "content_type", "created_by"],
        ]


class Cancellation(Modifiers):
    reason = models.TextField(null=True)
    booking_request = models.OneToOneField(
        BookingRequest, on_delete=models.CASCADE, related_name="cancel_booking_request"
    )

    class Meta:
        ordering = ["-created_at"]
