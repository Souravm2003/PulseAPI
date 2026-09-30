from django.db import models
from django.conf import settings


class Monitor(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="monitors"
    )

    name = models.CharField(max_length=100)

    url = models.URLField()

    method = models.CharField(
        max_length=10,
        default="GET"
    )

    expected_status = models.PositiveIntegerField(
        default=200
    )

    timeout = models.PositiveIntegerField(
        default=10
    )

    interval = models.PositiveIntegerField(
        default=5
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    last_checked_at = models.DateTimeField(
        null=True, blank=True
    )

    def __str__(self):
        return self.name