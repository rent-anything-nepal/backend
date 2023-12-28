from django.db import models
from django.contrib.auth import get_user_model

from utils.abstracts import Modifiers


class Province(models.Model):
    number = models.IntegerField(unique=True)
    name = models.CharField(max_length=255, unique=True)
    nepali_name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["number"]

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=255, unique=True)
    nepali_name = models.CharField(max_length=255, unique=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Municipality(Modifiers):
    name = models.CharField(max_length=255, unique=True)
    nepali_name = models.CharField(max_length=255, unique=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    longitude = models.FloatField()
    latitude = models.FloatField()
    average_rent_price = models.FloatField(default=0)
    total_accommodations = models.IntegerField(default=0)
    year_over_year_rent_change = models.FloatField(default=0)
    year_over_year_rent_change_percent = models.FloatField(default=0)
    rental_guide = models.TextField(default="")
    description = models.TextField(default="")
    is_approved = models.BooleanField(default=False, editable=False)
    approved_by = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, null=True,
        related_name="approved_%(class)s", editable=False
    )
    approved_at = models.DateTimeField(null=True, editable=False)

    class Meta:
        verbose_name_plural = "Municipalities"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Ward(models.Model):
    name = models.CharField(max_length=255)
    nepali_name = models.CharField(max_length=255)
    number = models.IntegerField()
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE)

    class Meta:
        ordering = ["name"]
        unique_together = [
            ["number", "municipality"],
            ["name", "municipality"],
            ["nepali_name", "municipality"]
        ]

    def __str__(self):
        return self.name
